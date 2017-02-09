"""
Checking whether users are players in tournaments, admins, organisers, etc.
"""

from testfixtures import compare

from models.authentication import PermissionDeniedException
from models.dao.account import Account, AccountSecurity
from models.dao.permissions import ProtectedObject, ProtObjAction, \
ProtObjPerm, AccountProtectedObjectPermission as AccountProtectedObjectPerm
from models.permissions import PermissionsChecker

from unit_tests.app_simulating_test import AppSimulatingTest

# pylint: disable=no-member,missing-docstring
class UserPermissions(AppSimulatingTest):

    acc_1 = 'test_add_account_creator'
    tourn_1 = 'test_user_permissions_tournament_1'

    # pylint: disable=invalid-name
    def setUp(self):
        super(UserPermissions, self).setUp()

        self.db.session.add(Account(self.acc_1, 'foo@bar.com'))
        self.db.session.add(AccountSecurity(self.acc_1, 'pwd1'))
        self.db.session.commit()
        self.injector.accounts.add(self.acc_1)

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
        self.assertFalse(Account.query.\
            filter_by(username=self.acc_1).first().is_superuser)

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
        tourn_prot_obj = self.injector.inject(self.tourn_1).get_dao().\
            protected_object
        player = '{}_player_1'.format(self.tourn_1)

        checker.add_permission(player, 'modify_application', tourn_prot_obj)
        prot_objs = ProtectedObject.query.count()
        prot_obj_actions = ProtObjAction.query.count()
        prot_obj_perms = ProtObjPerm.query.count()
        acc_perms = AccountProtectedObjectPerm.query.count()

        checker.remove_permission(player, 'modify_application', tourn_prot_obj)

        compare(prot_objs, ProtectedObject.query.count())
        compare(prot_obj_actions, ProtObjAction.query.count())
        compare(prot_obj_perms, ProtObjPerm.query.count())
        # the one account should now have lost it's permissions
        compare(acc_perms - 1, AccountProtectedObjectPerm.query.count())
