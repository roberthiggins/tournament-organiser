"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
from datetime import date, datetime
from json import dumps

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import and_

from models.authentication import PermissionDeniedException
from models.dao.db_connection import db
from models.dao.permissions import AccountProtectedObjectPermission, \
ProtectedObject, ProtObjPerm
from models.dao.registration import TournamentRegistration as Reg
from models.dao.score import ScoreCategory
from models.dao.table_allocation import TableAllocation
from models.dao.tournament import Tournament as TournamentDAO
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_round import TournamentRound as TR
from models.permissions import PermissionsChecker
from models.ranking_strategies import RankingStrategy
from models.tournament_draw import TournamentDraw, DrawException
from models.tournament_round import TournamentRound

def must_exist_in_db(func):
    """ A decorator that requires the tournament exists in the db"""
    def wrapped(self, *args, **kwargs): # pylint: disable=missing-docstring
        return func(self.check_exists(), *args, **kwargs)
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

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, tournament_id=None):
        self.tournament_id = tournament_id
        self.draw = TournamentDraw()
        self.ranking_strategy = RankingStrategy(tournament_id,
                                                self.get_score_categories)

    def check_exists(self):
        """Check that this Tournament has a corresponding DAO"""
        if self.get_dao() is None:
            print 'Tournament not found: {}'.format(self.tournament_id)
            raise ValueError('Tournament {} not found in database'.\
                format(self.tournament_id))
        return self

    def get_dao(self):
        """Convenience method to recover TournamentDAO"""
        return TournamentDAO.query.filter_by(name=self.tournament_id).first()


    @not_in_progress
    def delete(self):
        """Delete a tournament"""
        dao = self.get_dao()
        self.update({
            'rounds': 0,
            'score_categories': []
        })
        Reg.query.filter_by(tournament_id=dao.id).delete()
        TournamentEntry.query.filter_by(tournament_id=dao.name).delete()
        db.session.delete(dao)
        db.session.flush()
        AccountProtectedObjectPermission.query.\
            filter_by(account_username=dao.to_username).delete()
        ProtObjPerm.query.\
            filter_by(protected_object_id=dao.protected_object.id).delete()
        ProtectedObject.query.filter_by(id=dao.protected_object.id).\
            delete()
        db.session.commit()


    @not_in_progress
    def new(self, **details):
        """
        add a tournament to the db
        Expects:
            - details - dict of keys to put into the DAO
        """
        if self.get_dao() is not None:
            raise RuntimeError('A tournament with name {} already exists! ' \
            'Please choose another name'.format(self.tournament_id))

        dao = TournamentDAO(self.tournament_id)
        dao.to_username = details.pop('to_username')
        try:
            dao.date = datetime.strptime(details.pop('date'), self.DATE_FORMAT)
            if dao.date.date() < date.today():
                raise ValueError()
        except ValueError:
            raise ValueError('Enter a valid date')
        db.session.add(dao)
        db.session.commit()

        self._set_details(details)
        return self

    @must_exist_in_db
    @not_in_progress
    def confirm_entries(self):
        """ Check all the applications and create entries for all who qualify"""

        entries = [x.player_id for x in TournamentEntry.query.\
            filter_by(tournament_id=self.tournament_id).all()]

        pending_applications = Reg.query.filter(and_(
            Reg.tournament_id == self.get_dao().id,
            ~Reg.player_id.in_(entries))).all()

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
            'entries': self.get_dao().entries.count(),
            'rounds': self.get_dao().rounds.count(),
            'score_categories': self.get_score_categories(serialized=True)
        }


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
        if self.get_dao().rounds.count() == 0:
            raise ValueError('Please set the number of rounds for {} first'.\
                format(self.tournament_id))
        return [x.get_mission()
                for x in self.get_dao().rounds.order_by('ordering')]

    @must_exist_in_db
    def get_round(self, round_num):
        """Get the relevant TournamentRound"""
        if int(round_num) not in range(1, self.get_dao().rounds.count() + 1):
            raise ValueError('Tournament {} does not have a round {}'.format(
                self.tournament_id, round_num))

        return TournamentRound(self.tournament_id, round_num)

    @must_exist_in_db
    def get_score_categories(self, serialized=False):
        """
        List all the score categories available to this tournie and their
        percentages.

        If 'serialized' returns list of dicts rather than sqlalchemy objects:
        [{ 'name': 'Painting', 'percentage': 20, 'id': 1,
           'per_tournament': False }]
        """
        cats = ScoreCategory.query.\
            filter_by(tournament_id=self.tournament_id).all()
        return [{
            'id':             x.id,
            'name':           x.name,
            'percentage':     x.percentage,
            'per_tournament': x.per_tournament,
            'min_val':        x.min_val,
            'max_val':        x.max_val,
            'zero_sum':       x.zero_sum,
            'opponent_score': x.opponent_score
        } for x in cats] if serialized else cats


    @must_exist_in_db
    def make_draws(self):
        """Makes the draws for all rounds"""
        # If we can we determine all rounds
        if self.draw.matching_strategy.draw_for_all_rounds:
            for rnd in range(0, self.get_dao().rounds.count()):
                try:
                    model = self.get_round(rnd + 1)
                    self.draw.set_round(model)
                    self.draw.destroy_draw()
                    self.draw.set_entries(self.get_entries())
                    model.draw = self.draw.make_draw()
                except DrawException:
                    pass


    @must_exist_in_db
    def _set_details(self, details):
        """
        Set details for the tournament. Exceptions will be thrown when
        in_progress, etc.

        details should be a dict with optional keys:
            - date
            - missions
            - rounds
            - score_categories
            - to_username
        """
        dao = self.get_dao()

        if details.get('to_username', None) is not None and dao.in_progress:
            raise PROGRESS_EXCEPTION
        dao.creator_username = details.get('to_username', dao.to_username)

        if details.get('date', None) is not None and dao.in_progress:
            raise PROGRESS_EXCEPTION
        dao.date = details.get('date', dao.date)

        cats = details.get('score_categories', None)
        deserialised = [ScoreCategory(tournament_id=self.tournament_id, **x) \
            for x in cats] if cats is not None else None
        if cats is not None and self.get_score_categories() != deserialised:
            self._set_score_categories(cats)

        rounds = details.get('rounds')
        if rounds is not None:
            try:
                rounds = float(rounds)
            except ValueError:
                raise ValueError('Natural number required')
            if not rounds.is_integer() or rounds < 0:
                raise ValueError('Natural number required')
            if rounds != dao.rounds.count():
                self._set_rounds(rounds)

        missions = details.get('missions')
        if missions is not None and missions != self.get_missions():
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
            raise ValueError('Tournament {} has {} rounds. You submitted ' \
                'missions {}'.format(self.tournament_id, rounds,
                                     dumps([x for x in missions])))

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
    def _set_score_categories(self, new_categories):
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
            score_cats = self.get_dao().score_categories
            if len(keys) > 0: # we must keep some
                score_cats = score_cats.filter(~ScoreCategory.name.in_(keys))
            for cat in score_cats.all():
                for score in cat.scores:
                    score.game_scores.delete()
                    score.tournament_scores.delete()
                cat.scores.delete()
            score_cats.delete(synchronize_session='fetch')

            for cat in new_categories:
                dao = ScoreCategory.query.\
                    filter_by(tournament_id=self.tournament_id,
                              name=cat['name']).first()
                if dao is None:
                    dao = ScoreCategory(tournament_id=self.tournament_id, **cat)
                else:
                    dao.update(tournament_id=self.tournament_id, **cat)

                db.session.add(dao)
                db.session.flush()

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
    @not_in_progress
    def update(self, details):
        """Update the basic details about a tournament in the db"""
        self._set_details(details)


    @must_exist_in_db
    @not_in_progress
    def withdraw_entry(self, entry):
        """
        Withdraw an entry so they can no longer get scores, rankings, etc.

        If the round 1 draw has not been done yet:
            remove them from the list of entries
        If the tournament has begun:
            EXPLODE FOR NOW
            TODO: Handle during tournament withdrawals
        """
        entry.account.registrations.\
            filter_by(tournament_id=entry.tournament.id).delete()
        db.session.delete(entry)
        db.session.commit()


def all_tournaments_with_permission(action, username):
    """Find all tournaments where user has action. Returns list"""
    all_tournaments = TournamentDAO.query.\
        filter(TournamentDAO.date >= date.today()).\
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
