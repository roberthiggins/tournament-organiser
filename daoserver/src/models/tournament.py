"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import and_

from models.authentication import PermissionDeniedException
from models.dao.db_connection import db
from models.dao.registration import TournamentRegistration
from models.dao.score import ScoreCategory
from models.dao.table_allocation import TableAllocation
from models.dao.tournament import Tournament as TournamentDAO
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_round import TournamentRound as TR
from models.matching_strategy import RoundRobin
from models.permissions import PermissionsChecker, PERMISSIONS
from models.ranking_strategies import RankingStrategy
from models.score import upsert_tourn_score_cat, write_score
from models.table_strategy import ProtestAvoidanceStrategy
from models.tournament_round import TournamentRound, DrawException

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

def not_in_progress(func):
    """
    Decorator to intercept actions that cannot be performed on an in-progress
    tournament
    """
    def wrapped(self, *args, **kwargs): # pylint: disable=missing-docstring
        if self.get_dao() is not None and self.get_dao().in_progress:
            raise ValueError('You cannot perform this action on a tournament ' \
                             'that is in progress')
        return func(self, *args, **kwargs)
    return wrapped

# pylint: disable=no-member
class Tournament(object):
    """A tournament model"""

    def __init__(self, tournament_id=None, ranking_strategy=None):
        self.tournament_id = tournament_id
        self.exists_in_db = self.get_dao() is not None
        self.ranking_strategy = \
            ranking_strategy(tournament_id, self.list_score_categories) \
            if ranking_strategy \
            else RankingStrategy(tournament_id, self.list_score_categories)
        self.matching_strategy = RoundRobin()
        self.table_strategy = ProtestAvoidanceStrategy()
        self.creator_username = None
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

        dao = TournamentDAO(self.tournament_id)
        dao.creator_username = self.creator_username
        dao.date = self.date
        db.session.add(dao)

        PermissionsChecker().add_permission(
            self.creator_username,
            PERMISSIONS['ENTER_SCORE'],
            dao.protected_object)
        db.session.commit()

    def get_dao(self):
        """Convenience method to recover TournamentDAO"""
        return TournamentDAO.query.filter_by(name=self.tournament_id).first()

    @must_exist_in_db
    @not_in_progress
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

    @must_exist_in_db
    def get_missions(self):
        """Get all the missions for the tournament. List ordered by ordering"""
        return [x.get_mission()
                for x in self.get_dao().rounds.order_by('ordering')]

    @must_exist_in_db
    def get_num_rounds(self):
        """The number of rounds in the tournament"""
        return self.get_dao().rounds.count()

    @not_in_progress
    def set_date(self, date):
        """Set the date for the tournament"""
        try:
            self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
            if self.date.date() < datetime.date.today():
                raise ValueError()
        except ValueError:
            raise ValueError('Enter a valid date')

    @must_exist_in_db
    @not_in_progress
    def set_in_progress(self):
        """
        Attempt to mark the tournament as 'in progress'. After this point you
        are unable to set rounds, missions, score_categories, entries, etc.

        All those features need to have sane values for this to succeed.
        """
        if self.get_num_rounds() < 1:
            raise ValueError('You need to add at least 1 round')
        if len([x for x in self.get_missions() if x != 'TBA']) < 1:
            raise ValueError('You need to set the missions')
        if len(self.entries()) < 1:
            raise ValueError('You need at least 1 entrant')
        if len(self.list_score_categories()) < 1:
            raise ValueError('You need to set the score categories')

        self.get_dao().in_progress = True
        db.session.add(self.get_dao())
        db.session.commit()

    @must_exist_in_db
    def set_missions(self, missions=None):
        """ Set missions for tournament. Must set a mission for each round"""
        rounds = self.get_num_rounds()

        if missions is None or len(missions) != rounds:
            raise ValueError('Tournament {} has {} rounds. \
                You submitted missions {}'.\
                format(self.tournament_id, rounds, missions))

        for i, mission in enumerate(missions):
            rnd = self.get_round(i + 1).get_dao()
            rnd.mission = mission if mission is not None else rnd.get_mission()
            db.session.add(rnd)

        db.session.commit()
        return 'Missions set: {}'.format(missions)

    @must_exist_in_db
    @not_in_progress
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
            'rounds': self.get_num_rounds(),
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
    def make_draws(self):
        """Makes the draws for all rounds"""
        # If we can we determine all rounds
        if self.matching_strategy.DRAW_FOR_ALL_ROUNDS:
            for rnd in range(0, self.get_num_rounds()):
                try:
                    self.get_round(rnd + 1).destroy_draw()
                    self.get_round(rnd + 1).make_draw(self.entries())
                except DrawException:
                    pass

    @must_exist_in_db
    def get_round(self, round_num):
        """Get the relevant TournamentRound"""
        if int(round_num) not in range(1, self.get_num_rounds() + 1):
            raise ValueError('Tournament {} does not have a round {}'.format(
                self.tournament_id, round_num))

        return TournamentRound(self.tournament_id, round_num,
                               self.matching_strategy, self.table_strategy)

    @must_exist_in_db
    @not_in_progress
    def set_number_of_rounds(self, num_rounds):
        """Set the number of rounds in a tournament"""
        num_rounds = int(num_rounds)

        for rnd in self.get_dao().rounds.filter(TR.ordering > num_rounds).\
        order_by(TR.ordering.desc()).all():
            self.get_round(rnd.ordering).db_remove(False)

        for rnd in range(self.get_num_rounds(), num_rounds):
            db.session.add(TR(self.tournament_id, rnd + 1))

        db.session.commit()

        self.make_draws()

def all_tournaments_with_permission(action, username):
    """Find all tournaments where user has action. Returns list"""
    all_tournaments = TournamentDAO.query.\
        filter(TournamentDAO.date >= datetime.date.today()).\
        order_by(TournamentDAO.date.asc()).all()
    checker = PermissionsChecker()
    modifiable_tournaments = []

    for tourn in all_tournaments:
        try:
            if checker.check_permission(action, username, None, tourn.name):
                modifiable_tournaments.append(tourn.name)
        except PermissionDeniedException:
            pass

    return modifiable_tournaments
