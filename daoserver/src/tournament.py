"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
import datetime

from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.sql.expression import and_

from matching_strategy import RoundRobin
from models.db_connection import db
from models.game_entry import GameEntrant
from models.permissions import ProtObjAction, ProtObjPerm
from models.score import Score, ScoreCategory, ScoreKey, TournamentScore, \
GameScore
from models.table_allocation import TableAllocation
from models.tournament import Tournament as TournamentDB
from models.tournament_entry import TournamentEntry
from models.tournament_game import TournamentGame
from models.tournament_round import TournamentRound as TR
from permissions import PermissionsChecker, PERMISSIONS
from ranking_strategies import RankingStrategy
from table_strategy import ProtestAvoidanceStrategy

def must_exist_in_db(func):
    """ A decorator that requires the tournament exists in the db"""
    def wrapped(self, *args, **kwargs):                 # pylint: disable=missing-docstring
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

    def add_to_db(self, date):
        """
        add a tournament
        Expects:
            - inputTournamentDate - Tournament Date. YYYY-MM-DD
        """
        if self.exists_in_db:
            raise RuntimeError('A tournament with name {} already exists! \
            Please choose another name'.format(self.tournament_id))

        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        if date.date() < datetime.date.today():
            raise ValueError('Enter a valid date')

        dao = TournamentDB(self.tournament_id)
        dao.date = date
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
    def set_score_categories(self, new_categories):
        """
        Replace the existing score categories with those from the list. The list
        should contain a ScoreCategorys
        """

        # check for duplicates
        keys = [cat.display_name for cat in new_categories]
        if len(keys) != len(set(keys)):
            raise ValueError("You cannot set multiple keys with the same name")

        to_delete = ScoreCategory.query.\
            filter_by(tournament_id=self.tournament_id).all()

        for cat in new_categories:
            dao = ScoreCategory.query.\
                filter_by(tournament_id=self.tournament_id,
                          display_name=cat.display_name).first()

            if dao is None:
                dao = ScoreCategory(self.tournament_id,
                                    cat.display_name,
                                    cat.percentage,
                                    cat.per_tournament,
                                    cat.min_val,
                                    cat.max_val,)
            else:
                to_delete = [x for x in to_delete \
                if x.display_name != cat.display_name]
            dao.percentage = int(cat.percentage)
            dao.per_tournament = cat.per_tournament
            dao.clashes()
            db.session.add(dao)
            db.session.flush()

            try:
                if ScoreKey.query.filter_by(key=cat.display_name,
                                            category=dao.id).first() is None:
                    db.session.add(ScoreKey(cat.display_name, dao.id))
                    db.session.commit()
            except IntegrityError:
                raise Exception('Score already set')

        for cat in to_delete:
            cat.delete()

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
    def enter_score(self, entry_id, score_key, score, game_id=None):
        """
        Enters a score for category into tournament for player.

        Expects: All fields required
            - entry_id - of the entry
            - score_key - e.g. round_3_battle
            - score - integer

        Returns: Nothing on success. Throws ValueErrors and RuntimeErrors when
            there is an issue inserting the score.
        """
        # score_key should mean something in the context of the tournie
        key = db.session.query(ScoreKey).join(ScoreCategory).\
            filter(and_(ScoreCategory.tournament_id == self.get_dao().name,
                        ScoreKey.key == score_key)
                  ).first()

        # Validate the score
        try:
            score = int(score)
            if score < key.score_category.min_val or \
            score > key.score_category.max_val:
                raise ValueError()
        except ValueError:
            raise ValueError('Invalid score: {}'.format(score))
        except AttributeError:
            raise TypeError('Unknown category: {}'.format(score_key))

        # Has it already been entered?
        if game_id is None:
            existing_score = TournamentScore.query.join(Score).join(ScoreKey).\
                filter(and_(TournamentScore.entry_id == entry_id,
                            TournamentScore.tournament_id == self.get_dao().id,
                            ScoreKey.id == key.id)).first() is not None
        else:
            try:
                existing_score = GameScore.query.join(Score).\
                    filter(and_(GameScore.entry_id == entry_id, \
                                GameScore.game_id == game_id,
                                Score.score_key_id == key.id)).\
                    first() is not None
            except DataError:
                db.session.rollback()
                raise AttributeError('{} not entered. Game {} cannot be found'.\
                    format(score, game_id))

        if existing_score:
            raise ValueError(
                '{} not entered. Score is already set'.format(score))

        try:
            score_dao = Score(entry_id, key.id, score)
            db.session.add(score_dao)
            db.session.flush()

            if game_id is not None:
                db.session.add(GameScore(entry_id, game_id, score_dao.id))
            else:
                db.session.add(
                    TournamentScore(entry_id, self.get_dao().id, score_dao.id))
            db.session.commit()
        except IntegrityError as err:
            db.session.rollback()
            if 'is not present in table "entry"' in err.__repr__():
                raise AttributeError('{} not entered. Entry {} doesn\'t exist'.\
                    format(score, entry_id))
            elif 'is not present in table "game"' in err.__repr__():
                raise AttributeError('{} not entered. Game {} cannot be found'.\
                    format(score, game_id))
            raise err

    @staticmethod
    def is_score_entered(game_dao):
        """
        Determine if all the scores have been entered for this game.
        Not that, if false, the result will be double checked and possibly
        updated
        """
        if game_dao is not None and game_dao.score_entered:
            return True

        per_round_scores = len(game_dao.tournament_round.tournament.\
            score_categories.filter_by(per_tournament=False).all())
        if per_round_scores <= 0:
            raise AttributeError(
                '{} does not have any scores associated with it'.\
                format(game_dao))

        scores_expected = per_round_scores * len(game_dao.entrants.all())

        if len(game_dao.game_scores.all()) == scores_expected:
            game_dao.score_entered = True
            db.session.add(game_dao)
            db.session.commit()
            return True

        return False

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
                    'key': x.score_key.key,
                    'score': x.value,
                    'category': x.score_key.score_category.display_name,
                    'min_val': x.score_key.score_category.min_val,
                    'max_val': x.score_key.score_category.max_val,
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
        categories = ScoreCategory.query.\
            filter_by(tournament_id=self.tournament_id).all()
        return [
            {'id': x.id,
             'name': x.display_name,
             'percentage': x.percentage,
             'per_tournament': x.per_tournament,
             'min_val': x.min_val,
             'max_val': x.max_val} for x in categories]

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
            rnd.round_scores.delete()
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

# pylint: disable=too-many-arguments
class ScoreCategoryPair(object):
    """A holder object for score category information"""
    def __init__(self, name, percentage, per_tourn, min_val, max_val):
        if not name:
            raise ValueError('Category must have a name')

        try:
            self.percentage = int(percentage)
        except TypeError:
            raise ValueError('Percentage must be an integer (1-100)')

        try:
            self.min_val = int(min_val)
            self.max_val = int(max_val)
        except ValueError:
            raise ValueError('Min and Max Scores must be integers')
        except TypeError:
            raise ValueError('Min and Max Scores must be integers')

        self.display_name = name
        self.per_tournament = per_tourn
