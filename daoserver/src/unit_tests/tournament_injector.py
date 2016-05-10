"""
An injector to create tournaments for unit tests
"""
# pylint: disable=no-member

from datetime import datetime, timedelta

from models.account import Account
from models.db_connection import db, write_to_db
from models.registration import TournamentRegistration as TRegistration
from models.tournament import Tournament
from models.tournament_entry import TournamentEntry
from models.tournament_round import TournamentRound

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
        write_to_db(Account(username, email))
        TournamentEntry(username, tournament_name).write()
        self.accounts.add(username)

    def create_tournament(self, name, date, rounds=0):
        """Create a tournament"""
        tourn = Tournament(name)
        tourn.num_rounds = rounds
        tourn.date = date
        tourn.write()
        self.tournament_ids.add(tourn.id)
        self.tournament_names.add(tourn.name)

    def create_players(self, tourn_name, num_players):
        """Create some accounts and enter them in the tournament"""
        for entry_no in range(1, num_players + 1):
            player_name = '{}_player_{}'.format(tourn_name, entry_no)
            write_to_db(Account(player_name, '{}@test.com'.format(player_name)))
            TournamentEntry(player_name, tourn_name).write()
            self.accounts.add(player_name)

    def delete_scores(self):
        """Delete all scores for all tournaments injected"""

        for tourn in Tournament.query.filter(Tournament.id.in_(
                tuple(self.tournament_ids))).all():

            if tourn is None:
                return

            for rnd in tourn.rounds:
                rnd.round_scores.delete()

            for cat in tourn.score_categories:
                for key in cat.score_keys:
                    key.scores.delete()
                cat.score_keys.delete()
            tourn.score_categories.delete()
        db.session.commit()
