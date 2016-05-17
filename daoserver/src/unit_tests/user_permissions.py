"""
Checking whether users are players in tournaments, admins, organisers, etc.
"""

from flask.ext.testing import TestCase

from app import create_app
from models.account import db as account_db, Account, AccountSecurity, \
add_account
from permissions import PermissionsChecker

# pylint: disable=no-member,no-init,invalid-name,missing-docstring
class UserPermissions(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        account_db.create_all()
        self.acc_1 = 'test_add_account_admin'

    def tearDown(self):
        AccountSecurity.query.filter_by(id=self.acc_1).delete()
        Account.query.filter_by(username=self.acc_1).delete()
        account_db.session.commit()

        account_db.session.remove()

    def test_add_account(self):
        add_account(self.acc_1, 'foo@bar.com', 'pwd1')
        self.assertFalse(Account.query.\
            filter_by(username=self.acc_1).first().is_superuser)

    def test_is_player(self):
        """users can be a player by being involved in a game"""
        checker = PermissionsChecker()

        self.assertTrue(checker.is_game_player('lisa', 1))
        self.assertFalse(checker.is_game_player('lisa', 12))
        self.assertFalse(checker.is_game_player('superman', 1))
        self.assertFalse(checker.is_game_player('homer', 1))

    def test_is_organiser(self):
        """check if a user is an organiser"""
        checker = PermissionsChecker()

        options = [None, 'ranking_test', 'not_a_tournament', '', 'lisa', \
            'not_a_person', 'superman', 'permission_test', 'lex_luthor']

        for user in options:
            for tourn in options:
                if user == 'lex_luthor' and tourn == 'permission_test':
                    self.assertTrue(checker.is_organiser(user, tourn))
                else:
                    self.assertFalse(checker.is_organiser(user, tourn))

    def test_check_permissions(self):
        """Test the entrypoint method"""
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
        self.assertTrue(checker.check_permission(
            'enter_score',
            'lex_luthor',
            None,
            'permission_test'))
        self.assertTrue(checker.check_permission(
            'enter_score',
            'superman',
            None,
            'permission_test'))
        self.assertTrue(checker.check_permission(
            'enter_score',
            'permission_test_player',
            'permission_test_player',
            'permission_test'))
        self.assertFalse(checker.check_permission(
            'enter_score',
            'permission_test_player',
            'charlie_murphy',
            'permission_test'))
        self.assertFalse(checker.check_permission(
            'enter_score',
            'permission_test_player',
            None,
            'permission_test'))
        self.assertFalse(checker.check_permission(
            'enter_score',
            'charlie_murphy',
            None,
            'permission_test'))
