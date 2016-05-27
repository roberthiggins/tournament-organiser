"""
An injector to create tournaments for unit tests

If you want to check that this has cleaned up after itself you can run db-usage
or something similar to:

    SELECT schemaname,relname,n_live_tup
    FROM pg_stat_user_tables
    ORDER BY n_live_tup DESC;

"""
# pylint: disable=no-member

from datetime import datetime, timedelta

from models.account import Account
from models.db_connection import db
from models.permissions import AccountProtectedObjectPermission
from models.registration import TournamentRegistration as TRegistration
from models.tournament import Tournament
from models.tournament_entry import TournamentEntry
from models.tournament_round import TournamentRound

from permissions import PermissionsChecker, PERMISSIONS

class TournamentInjector(object):
    """Insert a tournament using the ORM. You can delete them as well"""

    def __init__(self):
        self.tournament_ids = set()
        self.tournament_names = set()
        self.accounts = set()

    def inject(self, name, rounds=0, num_players=6, date=None):
        """Create a tournament and inkect it into the db."""

        # To avoid clashes we shift default tournament into the future
        if date is None:
            date = datetime.now() + timedelta(weeks=len(self.tournament_ids))

        self.create_tournament(name, date, rounds)

        self.create_players(name, num_players)

        return

    def delete(self):
        """Remove all tournaments we have injected"""

        self.delete_scores()

        self.delete_games()

        # Some relations can't be deleted via relationship for some reason
        if len(self.accounts) > 0:
            # registrations and entries
            TRegistration.query.filter(
                TRegistration.tournament_id.in_(tuple(self.tournament_ids))).\
                delete(synchronize_session=False)
            TournamentEntry.query.filter(
                TournamentEntry.tournament_id.\
                in_(tuple(self.tournament_names))).\
                delete(synchronize_session=False)

            # Accounts
            AccountProtectedObjectPermission.query.filter(
                AccountProtectedObjectPermission.account_username.\
                in_(self.accounts)).delete(synchronize_session=False)
            Account.query.filter(
                Account.username.in_(tuple(self.accounts))).\
                delete(synchronize_session=False)
            self.accounts = set()

        if len(self.tournament_ids) > 0:
            TournamentRound.query.filter(TournamentRound.tournament_name.in_(
                tuple(self.tournament_names))).delete(synchronize_session=False)
            Tournament.query.filter(
                Tournament.id.in_(tuple(self.tournament_ids))).\
                delete(synchronize_session=False)
            self.tournament_ids = set()
            self.tournament_names = set()

        db.session.commit()
        return

    def add_player(self, tournament_name, username, email='foo@bar.com'):
        """Create player account and enter them"""
        db.session.add(Account(username, email))
        db.session.flush()
        db.session.add(TournamentEntry(username, tournament_name))
        db.session.flush()
        self.accounts.add(username)

    def add_round(self, tourn_name, round_num, mission):
        """Add a TournamentRound. Caller's job to ensure clash avoidance"""
        db.session.add(TournamentRound(tourn_name, int(round_num), mission))

    def create_tournament(self, name, date, rounds=0):
        """Create a tournament"""
        tourn = Tournament(name)
        tourn.num_rounds = rounds
        tourn.date = date
        db.session.add(tourn)
        db.session.flush()
        self.tournament_ids.add(tourn.id)
        self.tournament_names.add(tourn.name)

        creator_name = '{}_creator'.format(tourn.name)
        db.session.add(Account(creator_name, '{}@bar.com'.format(creator_name)))
        db.session.flush()
        self.accounts.add(creator_name)
        PermissionsChecker().add_permission(
            creator_name,
            PERMISSIONS['ENTER_SCORE'],
            tourn.protected_object)

    def create_players(self, tourn_name, num_players):
        """Create some accounts and enter them in the tournament"""
        for entry_no in range(1, num_players + 1):
            play_name = '{}_player_{}'.format(tourn_name, entry_no)
            db.session.add(Account(play_name, '{}@test.com'.format(play_name)))
            db.session.flush()
            db.session.add(TournamentEntry(play_name, tourn_name))
            db.session.flush()
            self.accounts.add(play_name)

    def delete_games(self):
        """
        Delete games and their entrants.
        Scores need to be deleted before calling.
        """
        for tourn in Tournament.query.filter(Tournament.id.in_(
                tuple(self.tournament_ids))).all():

            # remove all the game entrants.
            tourn_entries = TournamentEntry.query.filter(
                TournamentEntry.tournament_id.\
                in_(tuple(self.tournament_names))).all()
            for ent in tourn_entries:
                ent.game_entries.delete(synchronize_session=False)

            # Now the games
            for rnd in tourn.rounds:
                rnd.games.delete()

    def delete_scores(self):
        """Delete all scores for all tournaments injected"""

        for tourn in Tournament.query.filter(Tournament.id.in_(
                tuple(self.tournament_ids))).all():

            if tourn is None:
                return

            for rnd in tourn.rounds:
                rnd.round_scores.delete()

            tourn.tournament_scores.delete()

            for cat in tourn.score_categories:
                for key in cat.score_keys:
                    for score in key.scores:
                        score.game_scores.delete()
                    key.scores.delete()
                cat.score_keys.delete()
            tourn.score_categories.delete()
        db.session.commit()
