"""
Checking whether users are players in tournaments, admins, organisers, etc.
"""

from flask.ext.testing import TestCase

from app import create_app
from models.account import db, Account, AccountSecurity, add_account
from models.permissions import AccountProtectedObjectPermission
from permissions import PermissionsChecker

from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=no-member,no-init,invalid-name,missing-docstring
class UserPermissions(TestCase):

    acc_1 = 'test_add_account_creator'
    tourn_1 = 'test_user_permissions_tournament_1'

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()

    def tearDown(self):
        AccountProtectedObjectPermission.query.\
            filter(AccountProtectedObjectPermission.account_username == \
            self.acc_1).delete(synchronize_session=False)
        AccountSecurity.query.filter_by(id=self.acc_1).\
            delete(synchronize_session=False)
        Account.query.filter_by(username=self.acc_1).\
            delete(synchronize_session=False)
        db.session.commit()

        self.injector.delete()
        db.session.remove()

    def test_add_account(self):
        add_account(self.acc_1, 'foo@bar.com', 'pwd1', commit=False)
        self.assertFalse(Account.query.\
            filter_by(username=self.acc_1).first().is_superuser)

    def test_is_organiser(self):
        """check if a user is an organiser"""
        checker = PermissionsChecker()
        self.injector.inject(self.tourn_1)
        creator = '{}_creator'.format(self.tourn_1)

        options = [None, 'ranking_test', 'not_a_tournament', '', 'lisa', \
            'not_a_person', 'superman', 'permission_test', self.tourn_1, \
            creator]

        self.assertTrue(checker.is_organiser(creator, self.tourn_1))

        for user in options:
            for tourn in options:
                if user == creator and tourn == self.tourn_1:
                    self.assertTrue(checker.is_organiser(user, tourn))
                else:
                    self.assertFalse(checker.is_organiser(user, tourn))

    def test_superuser(self):
        """check if a user is an organiser"""
        checker = PermissionsChecker()
        add_account(self.acc_1, 'foo@bar.com', 'pwd1', commit=False)
        Account.query.filter_by(username=self.acc_1).first().is_superuser = True
        self.injector.inject(self.tourn_1)

        self.assertTrue(checker.check_permission(
            'enter_score',
            self.acc_1,
            None,
            self.tourn_1))

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
        add_account(self.acc_1, 'foo@bar.com', 'pwd1', commit=False) # random
        self.injector.inject(self.tourn_1, num_players=2)
        t_player_1 = '{}_player_1'.format(self.tourn_1)

        # player for themselves
        self.assertTrue(checker.check_permission(
            'enter_score',
            t_player_1,
            t_player_1,
            self.tourn_1))

        # player for random user
        self.assertFalse(checker.check_permission(
            'enter_score',
            t_player_1,
            self.acc_1,
            self.tourn_1))

        # player who is not superuser
        self.assertFalse(checker.check_permission(
            'enter_score',
            t_player_1,
            None,
            self.tourn_1))

        # random user
        self.assertFalse(checker.check_permission(
            'enter_score',
            self.acc_1,
            None,
            self.tourn_1))
