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

from models.dao.account import Account, AccountSecurity
from models.dao.db_connection import db
from models.dao.permissions import AccountProtectedObjectPermission, \
ProtectedObject, ProtObjAction, ProtObjPerm
from models.dao.registration import TournamentRegistration as TReg
from models.dao.tournament import Tournament
from models.dao.tournament_entry import TournamentEntry

from models.permissions import set_up_permissions
from models.tournament import Tournament as Tourn

class TournamentInjector(object):
    """Insert a tournament using the ORM. You can delete them as well"""

    def __init__(self):
        self.tournaments = set()
        self.accounts = set()
        self.existing_perms = set([o.id for o in ProtObjAction.query.all()])
        set_up_permissions()

    def inject(self, name, num_players=6, date=None, past_event=False):
        """Create a tournament and inkect it into the db."""

        # To avoid clashes we shift default tournament into the future
        if date is None:
            date = datetime.now() + timedelta(weeks=len(self.tournaments))

        self.create_tournament(name, date, past_event)

        self.create_players(name, num_players)

        return

    def delete(self):
        """Remove all tournaments we have injected"""

        for tourn in self.tournaments:
            dao = tourn.get_dao()
            dao.in_progress = False
            tourn.update({
                'rounds': 0,
                'score_categories': []
            })

        self.delete_accounts()

        self.delete_tournaments()

        if len(self.existing_perms):
            ProtObjAction.query.\
                filter(~ProtObjAction.id.in_(self.existing_perms)).\
                delete(synchronize_session=False)
            self.existing_perms = set()

        db.session.commit()

    def add_player(self, tournament_name, username, email='foo@bar.com'):
        """Create player account and enter them"""
        db.session.add(Account(username, email))
        db.session.flush()
        db.session.add(TournamentEntry(username, tournament_name))
        db.session.flush()
        self.accounts.add(username)

    def create_tournament(self, name, date, past_event=False):
        """Create a tournament"""
        to_username = '{}_creator'.format(name)
        db.session.add(Account(to_username, '{}@bar.com'.format(to_username)))
        db.session.flush()

        if past_event:
            # We need to do this by hand with the daos
            dao = Tournament(name)
            dao.date = date
            dao.to_username = to_username
            db.session.add(dao)
            db.session.commit()

            tourn = Tourn(name)
        else:
            tourn = Tourn(name).new({
                'date': date.strftime(Tourn.DATE_FORMAT),
                'to_username': to_username
            })

        self.tournaments.add(tourn)

    def create_players(self, tourn_name, num_players):
        """Create some accounts and enter them in the tournament"""
        for entry_no in range(1, num_players + 1):
            play_name = '{}_player_{}'.format(tourn_name, entry_no)
            db.session.add(Account(play_name, '{}@test.com'.format(play_name)))
            db.session.flush()
            db.session.add(TournamentEntry(play_name, tourn_name))
            db.session.flush()
            self.accounts.add(play_name)

    def delete_accounts(self):
        """Delete user accounts and sundry we have injected"""
        if not len(self.accounts):
            return

        # Some relations can't be deleted via relationship for some reason
        # registrations and entries
        if len(self.tournaments):
            ids = [t.get_dao().id for t in self.tournaments]
            TReg.query.filter(TReg.tournament_id.in_(ids)).\
                delete(synchronize_session=False)
            names = [t.get_dao().name for t in self.tournaments]
            TournamentEntry.query.filter(
                TournamentEntry.tournament_id.in_(names)).\
                delete(synchronize_session=False)

        # Accounts
        AccountProtectedObjectPermission.query.filter(
            AccountProtectedObjectPermission.account_username.\
            in_(self.accounts)).delete(synchronize_session=False)
        AccountSecurity.query.filter(AccountSecurity.id.in_(self.accounts)).\
            delete(synchronize_session=False)
        Account.query.filter(Account.username.in_(self.accounts)).\
            delete(synchronize_session=False)

        self.accounts = set()

    def delete_tournaments(self):
        """Delete tournaments and their rounds"""

        if not len(self.tournaments):
            return

        tourns = [t.get_dao() for t in self.tournaments]
        permission_ids = [t.protected_object.id for t in tourns]
        creators = Account.query.filter(
            Account.username.in_([t.to_username for t in tourns]))
        Tournament.query.filter(Tournament.id.in_([t.id for t in tourns])).\
            delete(synchronize_session=False)
        if creators.count() > 0:
            AccountProtectedObjectPermission.query.filter(
                AccountProtectedObjectPermission.account_username.\
                in_([c.username for c in creators.all()])).\
                delete(synchronize_session=False)
        if len(permission_ids) > 0:
            ProtObjPerm.query.\
                filter(ProtObjPerm.protected_object_id.in_(permission_ids)).\
                delete(synchronize_session=False)
            ProtectedObject.query.\
                filter(ProtectedObject.id.in_(permission_ids)).\
                delete(synchronize_session=False)
        creators.delete(synchronize_session=False)

        self.tournaments = set()

# pylint: disable=too-many-arguments
def score_cat_args(name, pct, per_tourn, min_val, max_val, zero_sum=False):
    """Convenience function to make a ScoreCategory args blob"""
    return {
        'name':           name,
        'percentage':     pct,
        'per_tournament': per_tourn,
        'min_val':        min_val,
        'max_val':        max_val,
        'zero_sum':       zero_sum}
