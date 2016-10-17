"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
import datetime

from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.sql.expression import and_

from models.authentication import PermissionDeniedException
from models.dao.db_connection import db
from models.dao.game_entry import GameEntrant
from models.dao.registration import TournamentRegistration
from models.dao.score import ScoreCategory
from models.dao.table_allocation import TableAllocation
from models.dao.tournament import Tournament as TournamentDAO
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_game import TournamentGame
from models.dao.tournament_round import TournamentRound as TR
from models.matching_strategy import RoundRobin
from models.permissions import PermissionsChecker
from models.ranking_strategies import RankingStrategy
from models.score import upsert_tourn_score_cat, validate_score, write_score
from models.table_strategy import ProtestAvoidanceStrategy
from models.tournament_round import TournamentRound, DrawException

def must_exist_in_db(func):
    """ A decorator that requires the tournament exists in the db"""
    def wrapped(self, *args, **kwargs): # pylint: disable=missing-docstring
        if self.get_dao() is None:
            print 'Tournament not found: {}'.format(self.tournament_id)
            raise ValueError(
                'Tournament {} not found in database'.format(
                    self.tournament_id))
        return func(self, *args, **kwargs)
    return wrapped

PROGRESS_EXCEPTION = ValueError('You cannot perform this action on a '\
                                'tournament that is in progress')
def not_in_progress(func):
    """
    Decorator to intercept actions that cannot be performed on an in-progress
    tournament
    """
    def wrapped(self, *args, **kwargs): # pylint: disable=missing-docstring
        if self.get_dao() is not None and self.get_dao().in_progress:
            raise PROGRESS_EXCEPTION
        return func(self, *args, **kwargs)
    return wrapped

# pylint: disable=no-member
class Tournament(object):
    """A tournament model"""

    def __init__(self, tournament_id=None):
        self.tournament_id = tournament_id
        self.matching_strategy = RoundRobin()
        self.table_strategy = ProtestAvoidanceStrategy()
        self.ranking_strategy = RankingStrategy(tournament_id,
                                                self.get_score_categories)


    def get_dao(self):
        """Convenience method to recover TournamentDAO"""
        return TournamentDAO.query.filter_by(name=self.tournament_id).first()


    @not_in_progress
    def new(self, details):
        """
        add a tournament to the db
        Expects:
            - details - dict of keys to put into the DAO
        """
        if self.get_dao() is not None:
            raise RuntimeError('A tournament with name {} already exists! \
            Please choose another name'.format(self.tournament_id))

        dao = TournamentDAO(self.tournament_id)
        dao.to_username = details.pop('to_username')
        try:
            date = datetime.datetime.strptime(details.pop('date'), "%Y-%m-%d")
            if date.date() < datetime.date.today():
                raise ValueError()
            dao.date = date
        except ValueError:
            raise ValueError('Enter a valid date')
        db.session.add(dao)
        db.session.commit()

        self.set_details(details)

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
    def details(self):
        """
        Get details about a tournament. This includes entrants and format
        information
        """
        details = self.get_dao()

        return {
            'name': details.name,
            'date': details.date,
            'rounds': self.get_dao().rounds.count(),
        }


    @must_exist_in_db
    def enter_score(self, entry_id, score_cat, score, game_id=None):
        """Enter a score for score_cat into self for entry."""
        entry = TournamentEntry.query.filter_by(id=entry_id).first()
        if entry is None:
            raise ValueError('Unknown entrant: {}'.format(entry_id))

        cat = db.session.query(ScoreCategory).filter_by(
            tournament_id=self.tournament_id, name=score_cat).first()
        try:
            game = TournamentGame.query.filter_by(id=game_id).first()
        except DataError:
            db.session.rollback()
            raise TypeError('{} not entered. Game {} cannot be found'.\
                format(score, game_id))
        try:
            validate_score(score, cat, entry, game)
        except AttributeError:
            raise TypeError('Unknown category: {}'.format(score_cat))

        if cat.opponent_score:
            entry = game.entrants.filter(GameEntrant.entrant_id != entry.id).\
                first().entrant

        write_score(self.get_dao(), entry, cat, score, game)
        return 'Score entered for {}: {}'.format(entry.player_id, score)


    @must_exist_in_db
    def get_entries(self):
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
    def get_missions(self):
        """Get all the missions for the tournament. List ordered by ordering"""
        return [x.get_mission()
                for x in self.get_dao().rounds.order_by('ordering')]

    @must_exist_in_db
    def get_round(self, round_num):
        """Get the relevant TournamentRound"""
        if int(round_num) not in range(1, self.get_dao().rounds.count() + 1):
            raise ValueError('Tournament {} does not have a round {}'.format(
                self.tournament_id, round_num))

        return TournamentRound(self.tournament_id, round_num,
                               self.matching_strategy, self.table_strategy)

    @must_exist_in_db
    def get_score_categories(self):
        """
        List all the score categories available to this tournie and their
        percentages.
        [{ 'name': 'Painting', 'percentage': 20, 'id': 1,
           'per_tournament': False }]
        """
        return ScoreCategory.query.\
            filter_by(tournament_id=self.tournament_id).all()


    def set_details(self, details):
        """
        Set details for the tournament. Exceptions will be thrown when
        in_progress, etc.

        details should be a dict with optional keys:
            - date
            - missions
            - rounds
            - to_username
        """
        dao = self.get_dao()

        if details.get('to_username', None) is not None and dao.in_progress:
            raise PROGRESS_EXCEPTION
        dao.creator_username = details.get('to_username', dao.to_username)

        if details.get('date', None) is not None and dao.in_progress:
            raise PROGRESS_EXCEPTION
        dao.date = details.get('date', dao.date)

        rounds = details.get('rounds', dao.rounds.count())
        if rounds != dao.rounds.count():
            self._set_rounds(rounds)

        missions = details.get('missions', self.get_missions())
        if missions != self.get_missions():
            self._set_missions(missions)

        db.session.add(dao)
        db.session.commit()


    @must_exist_in_db
    @not_in_progress
    def set_in_progress(self):
        """
        Attempt to mark the tournament as 'in progress'. After this point you
        are unable to set rounds, missions, score_categories, entries, etc.

        All those features need to have sane values for this to succeed.
        """
        if self.get_dao().rounds.count() < 1:
            raise ValueError('You need to add at least 1 round')
        if len([x for x in self.get_missions() if x != 'TBA']) < 1:
            raise ValueError('You need to set the missions')
        if len(self.get_entries()) < 1:
            raise ValueError('You need at least 1 entrant')
        if len(self.get_score_categories()) < 1:
            raise ValueError('You need to set the score categories')

        self.get_dao().in_progress = True
        db.session.add(self.get_dao())
        db.session.commit()

    @must_exist_in_db
    def _set_missions(self, missions=None):
        """ Set missions for tournament. Must set a mission for each round"""
        rounds = self.get_dao().rounds.count()

        if missions is None or len(missions) != rounds:
            raise ValueError('Tournament {} has {} rounds. \
                You submitted missions {}'.\
                format(self.tournament_id, rounds, missions))

        for i, mission in enumerate(missions):
            rnd = self.get_round(i + 1).get_dao()
            rnd.mission = mission if mission is not None else rnd.get_mission()
            db.session.add(rnd)

        db.session.commit()


    @must_exist_in_db
    @not_in_progress
    def _set_rounds(self, num_rounds):
        """Set the number of rounds in a tournament"""
        num_rounds = int(num_rounds)

        for rnd in self.get_dao().rounds.filter(TR.ordering > num_rounds).\
        order_by(TR.ordering.desc()).all():
            self.get_round(rnd.ordering).db_remove(False)

        for rnd in range(self.get_dao().rounds.count(), num_rounds):
            db.session.add(TR(self.tournament_id, rnd + 1))

        db.session.commit()

        self.make_draws()


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
            ScoreCategory.query.filter(and_(
                ScoreCategory.tournament_id == self.tournament_id,
                ~ScoreCategory.name.in_(keys)
            )).delete(synchronize_session='fetch')

            for cat in new_categories:
                upsert_tourn_score_cat(self.tournament_id, cat)
                ScoreCategory.query.\
                    filter_by(tournament_id=self.tournament_id,
                              name=cat['name']).first().clashes()

            db.session.commit()
        except ValueError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise


    @must_exist_in_db
    def make_draws(self):
        """Makes the draws for all rounds"""
        # If we can we determine all rounds
        if self.matching_strategy.DRAW_FOR_ALL_ROUNDS:
            for rnd in range(0, self.get_dao().rounds.count()):
                try:
                    self.get_round(rnd + 1).destroy_draw()
                    self.get_round(rnd + 1).make_draw(self.get_entries())
                except DrawException:
                    pass

    @must_exist_in_db
    @not_in_progress
    def update(self, details):
        """Update the basic details about a tournament in the db"""
        self.set_details(details)

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
