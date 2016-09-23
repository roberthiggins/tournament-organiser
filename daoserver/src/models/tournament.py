"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import and_

from models.dao.db_connection import db
from models.dao.game_entry import GameEntrant
from models.dao.permissions import ProtObjAction, ProtObjPerm
from models.dao.registration import TournamentRegistration
from models.dao.score import ScoreCategory
from models.dao.table_allocation import TableAllocation
from models.dao.tournament import Tournament as TournamentDB
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_game import TournamentGame
from models.dao.tournament_round import TournamentRound as TR
from models.matching_strategy import RoundRobin
from models.permissions import PermissionsChecker, PERMISSIONS
from models.ranking_strategies import RankingStrategy
from models.score import upsert_tourn_score_cat, write_score
from models.table_strategy import ProtestAvoidanceStrategy

def must_exist_in_db(func):
    """ A decorator that requires the tournament exists in the db"""
    def wrapped(self, *args, **kwargs): # pylint: disable=missing-docstring
        if not self.exists_in_db:
            print 'Tournament not found: {}'.format(self.tournament_id)
            raise ValueError(
                'Tournament {} not found in database'.format(
                    self.tournament_id))
        return func(self, *args, **kwargs)
    return wrapped

# pylint: disable=no-member
class Tournament(object):
    """A tournament DAO"""

    def __init__(self, tournament_id=None, ranking_strategy=None, creator=None):
        self.tournament_id = tournament_id
        self.exists_in_db = self.get_dao() is not None
        self.ranking_strategy = \
            ranking_strategy(tournament_id, self.list_score_categories) \
            if ranking_strategy \
            else RankingStrategy(tournament_id, self.list_score_categories)
        self.matching_strategy = RoundRobin()
        self.table_strategy = ProtestAvoidanceStrategy()
        self.creator_username = creator
        self.date = None

    def add_to_db(self):
        """
        add a tournament
        Expects:
            - inputTournamentDate - Tournament Date. YYYY-MM-DD
        """
        if self.exists_in_db:
            raise RuntimeError('A tournament with name {} already exists! \
            Please choose another name'.format(self.tournament_id))

        dao = TournamentDB(self.tournament_id)
        dao.date = self.date
        db.session.add(dao)

        if self.creator_username is not None:
            PermissionsChecker().add_permission(
                self.creator_username,
                PERMISSIONS['ENTER_SCORE'],
                dao.protected_object)
        db.session.commit()

    def get_dao(self):
        """Convenience method to recover DAO"""
        return TournamentDB.query.filter_by(name=self.tournament_id).first()

    @must_exist_in_db
    def confirm_entries(self):
        """ Check all the applications and create entries for all who qualify"""

        entries = [x.player_id for x in TournamentEntry.query.\
            filter_by(tournament_id=self.tournament_id).all()]

        pending_applications = TournamentRegistration.query.filter(and_(
            TournamentRegistration.tournament_id == self.get_dao().id,
            ~TournamentRegistration.player_id.in_(entries))).all()

        for app in pending_applications:
            try:
                dao = TournamentEntry(app.player_id, self.tournament_id)
                db.session.add(dao)
            except IntegrityError:
                pass
        db.session.commit()

    def set_date(self, date):
        """Set the date for the tournament"""
        try:
            self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
            if self.date.date() < datetime.date.today():
                raise ValueError()
        except ValueError:
            raise ValueError('Enter a valid date')

    @must_exist_in_db
    def set_score_categories(self, new_categories):
        """
        Replace the existing score categories with those from the list. The list
        should contain a ScoreCategorys
        """

        # check for duplicates
        keys = [cat['name'] for cat in new_categories]
        if len(keys) != len(set(keys)):
            raise ValueError("You cannot set multiple keys with the same name")

        # pylint: disable=broad-except
        try:
            # Delete the ones no longer needed
            to_delete = ScoreCategory.query.\
                filter(and_(ScoreCategory.tournament_id == self.tournament_id,
                            ~ScoreCategory.name.in_(keys)))
            to_delete.delete(synchronize_session='fetch')


            for cat in new_categories:
                upsert_tourn_score_cat(self.tournament_id, cat)

            # check for clashes before actually writing
            for cat in new_categories:
                ScoreCategory.query.\
                    filter_by(tournament_id=self.tournament_id,
                              name=cat['name']).first().clashes()

            db.session.commit()
        except ValueError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()

    @must_exist_in_db
    def details(self):
        """
        Get details about a tournament. This includes entrants and format
        information
        """
        details = self.get_dao()

        return {
            'name': details.name,
            'date': details.date,
            'rounds': details.num_rounds,
        }

    @must_exist_in_db
    def enter_score(self, entry_id, score_cat, score, game_id=None):
        """Enter a score for score_cat into self for entry."""
        write_score(self.get_dao(), entry_id, score_cat, score, game_id)

    @must_exist_in_db
    def entries(self):
        """Get a list of Entry"""

        entries = TournamentEntry.query.\
            filter_by(tournament_id=self.tournament_id).all()
        for entry in entries:
            entry.game_history = [x.table_no for x in \
                TableAllocation.query.filter_by(entry_id=entry.id)]
            entry.score_info = [
                {
                    'score': x.value,
                    'category': x.score_category.name,
                    'min_val': x.score_category.min_val,
                    'max_val': x.score_category.max_val,
                } for x in entry.scores
            ]

        return entries

    @must_exist_in_db
    def get_game_dao(self, round_num, table_num):
        """
        Get game_dao given table_num and round_num
        """
        return TournamentGame.query.join(TR).filter(
            and_(TR.ordering == round_num,
                 TournamentGame.table_num == table_num)).first()


    @must_exist_in_db
    def list_score_categories(self):
        """
        List all the score categories available to this tournie and their
        percentages.
        [{ 'name': 'Painting', 'percentage': 20, 'id': 1,
           'per_tournament': False }]
        """
        return ScoreCategory.query.\
            filter_by(tournament_id=self.tournament_id).all()

    @must_exist_in_db
    def make_draw(self, round_id=1):
        """Determines the draw for round. This draw is written to the db"""

        rnd = self.get_round(round_id)
        match_ups = self.matching_strategy.match(rnd.ordering, self.entries())
        draw = self.table_strategy.determine_tables(match_ups)
        for match in draw:

            entrants = [None if x == 'BYE' else x for x in match.entrants]

            game = TournamentGame.query.filter_by(
                tournament_round_id=rnd.id,
                table_num=match.table_number).first()
            if game is None:
                game = TournamentGame(rnd.id, match.table_number)
                db.session.add(game)
                db.session.flush()

            for entrant in entrants:
                if entrant is not None:
                    dao = TournamentEntry.query.\
                        filter_by(id=entrant.id).first()
                    game_entrant = GameEntrant.query.filter_by(
                        game_id=game.id, entrant_id=dao.id).first()
                    if game_entrant is None:
                        db.session.add(GameEntrant(game.id, dao.id))
                        PermissionsChecker().add_permission(
                            dao.player_id,
                            PERMISSIONS['ENTER_SCORE'],
                            game.protected_object)
                else:
                    # The person playing the bye gets no points at the time
                    game.score_entered = True
                    db.session.add(game)

        db.session.commit()
        return draw

    @must_exist_in_db
    def get_round(self, round_num):
        """Get the relevant TournamentRound"""
        if int(round_num) not in range(1, self.get_dao().num_rounds + 1):
            raise ValueError('Tournament {} does not have a round {}'.format(
                self.tournament_id, round_num))

        return self.get_dao().rounds.filter_by(ordering=round_num).first()

    @must_exist_in_db
    def set_number_of_rounds(self, num_rounds):
        """Set the number of rounds in a tournament"""
        tourn = self.get_dao()
        tourn.num_rounds = int(num_rounds)
        db.session.add(tourn)

        for rnd in tourn.rounds.filter(TR.ordering > tourn.num_rounds).all():
            for game in rnd.games:
                entrants = GameEntrant.query.filter_by(game_id=game.id)
                for entrant in entrants.all():
                    PermissionsChecker().remove_permission(
                        entrant.entrant.player_id,
                        PERMISSIONS['ENTER_SCORE'],
                        game.protected_object)
                entrants.delete()
                act_id = ProtObjAction.query.\
                    filter_by(description=PERMISSIONS['ENTER_SCORE']).first().id
                ProtObjPerm.query.filter_by(
                    protected_object_id=game.protected_object.id,
                    protected_object_action_id=act_id).delete()
                prot_obj = game.protected_object
                db.session.delete(game)
                db.session.delete(prot_obj)

        tourn.rounds.filter(TR.ordering > tourn.num_rounds).delete()
        db.session.flush()

        existing_rnds = len(tourn.rounds.filter().all())
        for rnd in range(existing_rnds + 1, tourn.num_rounds + 1):
            db.session.add(TR(self.tournament_id, rnd))
        db.session.commit()

        # If we can we determine all rounds
        if self.matching_strategy.DRAW_FOR_ALL_ROUNDS:
            for rnd in self.get_dao().rounds:
                self.make_draw(rnd.ordering)
