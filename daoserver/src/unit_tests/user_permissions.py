"""
Checking whether users are players in tournaments, admins, organisers, etc.
"""

from flask.ext.testing import TestCase

from app import create_app
from models.account import db as account_db, Account, AccountSecurity, \
add_account
from models.permissions import AccountProtectedObjectPermission
from models.tournament import Tournament as TournamentDAO
from permissions import PermissionsChecker
from tournament import Tournament

# pylint: disable=no-member,no-init,invalid-name,missing-docstring
class UserPermissions(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        account_db.create_all()
        self.acc_1 = 'test_add_account_creator'
        self.acc_2 = 'test_add_account_admin'
        self.accounts = [self.acc_1, self.acc_2]
        self.tourn_1 = 'test_user_permissions_tournament_1'
        self.tourn_2 = 'test_user_permissions_tournament_2'

    def tearDown(self):
        AccountProtectedObjectPermission.query.\
            filter(AccountProtectedObjectPermission.account_username.\
                   in_(self.accounts)).delete(synchronize_session=False)
        AccountSecurity.query.\
            filter(AccountSecurity.id.in_(self.accounts)).\
            delete(synchronize_session=False)
        Account.query.filter(Account.username.in_(self.accounts)).\
            delete(synchronize_session=False)
        TournamentDAO.query.filter_by(name=self.tourn_1).delete()
        TournamentDAO.query.filter_by(name=self.tourn_2).delete()
        account_db.session.commit()

        account_db.session.remove()

    def test_add_account(self):
        add_account(self.acc_1, 'foo@bar.com', 'pwd1')
        self.assertFalse(Account.query.\
            filter_by(username=self.acc_1).first().is_superuser)

    def test_is_organiser(self):
        """check if a user is an organiser"""
        checker = PermissionsChecker()
        add_account(self.acc_1, 'foo@bar.com', 'pwd1')
        Tournament(self.tourn_1, creator=self.acc_1).add_to_db('2110-12-25')
        options = [None, 'ranking_test', 'not_a_tournament', '', 'lisa', \
            'not_a_person', 'superman', 'permission_test', self.tourn_1, \
            self.acc_1]

        self.assertTrue(checker.is_organiser(self.acc_1, self.tourn_1))

        for user in options:
            for tourn in options:
                if user == self.acc_1 and tourn == self.tourn_1:
                    self.assertTrue(checker.is_organiser(user, tourn))
                else:
                    self.assertFalse(checker.is_organiser(user, tourn))

    def test_superuser(self):
        """check if a user is an organiser"""
        checker = PermissionsChecker()
        add_account(self.acc_1, 'foo@bar.com', 'pwd1')
        add_account(self.acc_2, 'foo@bar.com', 'pwd1')
        Account.query.filter_by(username=self.acc_2).first().is_superuser = True

        Tournament(self.tourn_1, creator=self.acc_1).add_to_db('2110-12-25')
        Tournament(self.tourn_2).add_to_db('2110-12-25')
        self.assertTrue(checker.check_permission(
            'enter_score',
            self.acc_2,
            None,
            self.tourn_1))
        self.assertTrue(checker.check_permission(
            'enter_score',
            self.acc_2,
            None,
            self.tourn_2))

    def test_check_permissions_bad_values(self):
        """malformed values"""
        checker = PermissionsChecker()
        self.assertRaises(
            ValueError, checker.check_permission, None, None, None, None)
        self.assertRaises(
            ValueError, checker.check_permission, '', None, None, None)
        self.assertRaises(ValueError, checker.check_permission, 'not_a_list',
                          None, None, None)
        self.assertRaises(ValueError, checker.check_permission, 'ENTER_SCORE',
                          None, None, None)

        self.assertFalse(checker.check_permission(
            'enter_score',
            None,
            None,
            None))

    def test_check_permissions(self):
        """Test the entrypoint method"""
        checker = PermissionsChecker()

        # player for themselves
        self.assertTrue(checker.check_permission(
            'enter_score',
            'permission_test_player',
            'permission_test_player',
            'permission_test'))

        # player for random user
        self.assertFalse(checker.check_permission(
            'enter_score',
            'permission_test_player',
            'charlie_murphy',
            'permission_test'))

        # player who is not superuser
        self.assertFalse(checker.check_permission(
            'enter_score',
            'permission_test_player',
            None,
            'permission_test'))

        # random user
        self.assertFalse(checker.check_permission(
            'enter_score',
            'charlie_murphy',
            None,
            'permission_test'))
