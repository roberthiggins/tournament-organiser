"""
Checking whether users are players in tournaments, admins, organisers, etc.
"""

from flask_testing import TestCase
from testfixtures import compare

from app import create_app
from models.authentication import PermissionDeniedException
from models.dao.account import db, Account, AccountSecurity
from models.dao.permissions import ProtectedObject, ProtObjAction, \
ProtObjPerm, AccountProtectedObjectPermission as AccountProtectedObjectPerm
from models.permissions import PermissionsChecker
from models.tournament import Tournament

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

        db.session.add(Account(self.acc_1, 'foo@bar.com'))
        db.session.add(AccountSecurity(self.acc_1, 'pwd1'))
        db.session.commit()

    def tearDown(self):
        AccountProtectedObjectPerm.query.\
            filter(AccountProtectedObjectPerm.account_username == self.acc_1).\
            delete(synchronize_session=False)
        AccountSecurity.query.filter_by(id=self.acc_1).\
            delete(synchronize_session=False)
        Account.query.filter_by(username=self.acc_1).\
            delete(synchronize_session=False)
        db.session.commit()

        self.injector.delete()
        db.session.remove()

    def test_add_account(self):
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

        self.assertRaises(PermissionDeniedException,
                          checker.check_permission,
                          'enter_score',
                          None,
                          None,
                          None)

    def test_check_permissions(self):
        """Test the entrypoint method"""
        checker = PermissionsChecker()
        self.injector.inject(self.tourn_1, num_players=2)
        t_player_1 = '{}_player_1'.format(self.tourn_1)

        # player for themselves
        self.assertTrue(checker.check_permission(
            'enter_score',
            t_player_1,
            t_player_1,
            self.tourn_1))

        # player for random user
        self.assertRaises(PermissionDeniedException,
                          checker.check_permission,
                          'enter_score',
                          t_player_1,
                          self.acc_1,
                          self.tourn_1)

        # player who is not superuser
        self.assertRaises(PermissionDeniedException,
                          checker.check_permission,
                          'enter_score',
                          t_player_1,
                          None,
                          self.tourn_1)

        # random user
        self.assertRaises(PermissionDeniedException,
                          checker.check_permission,
                          'enter_score',
                          self.acc_1,
                          None,
                          self.tourn_1)

    def test_remove_permissions(self):
        """Test that users can have their permissions removed"""

        checker = PermissionsChecker()
        self.injector.inject(self.tourn_1)
        creator = '{}_creator'.format(self.tourn_1)
        tourn_prot_obj = Tournament(self.tourn_1).get_dao().protected_object

        prot_objs = len(ProtectedObject.query.all())
        prot_obj_actions = len(ProtObjAction.query.all())
        prot_obj_perms = len(ProtObjPerm.query.all())
        acc_perms = len(AccountProtectedObjectPerm.query.all())

        self.assertTrue(checker.is_organiser(creator, self.tourn_1))
        checker.remove_permission(creator, 'enter_score', tourn_prot_obj)
        self.assertFalse(checker.is_organiser(creator, self.tourn_1))
        compare(prot_objs, len(ProtectedObject.query.all()))
        compare(prot_obj_actions, len(ProtObjAction.query.all()))
        compare(prot_obj_perms, len(ProtObjPerm.query.all()))
        # the one account should now have lost it's permissions
        compare(acc_perms - 1, len(AccountProtectedObjectPerm.query.all()))
