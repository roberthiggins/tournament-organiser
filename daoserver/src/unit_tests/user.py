"""
Checking whether users are players in tournaments, admins, organisers, etc.
"""

from datetime import date, timedelta
from testfixtures import compare

from models.dao.account import Account as Acc
from models.dao.tournament_entry import TournamentEntry as Entry
from models.user import User

from unit_tests.app_simulating_test import AppSimulatingTest

# pylint: disable=no-member,missing-docstring
class UserTests(AppSimulatingTest):

    def setUp(self):
        super(UserTests, self).setUp()

        self.player = 'player_1'
        today = date.today()

        self.injector.inject('yesterday', date=today - timedelta(days=1),
                             past_event=True)
        self.injector.inject('today', date=today)
        self.injector.inject('tomorrow', date=today + timedelta(days=1))
        self.db.session.add(Acc(self.player, '{}@bar.com'.format(self.player)))
        self.db.session.add(Entry(self.player, 'yesterday'))
        self.db.session.add(Entry(self.player, 'today'))
        self.db.session.add(Entry(self.player, 'tomorrow'))
        self.injector.accounts.add(self.player)

    def test_get_last_tournament(self):
        compare(User(self.player).get_last_tournament().name, 'today')

    def test_get_next_tournament(self):
        compare(User(self.player).get_next_tournament().name, 'today')

    def test_update(self):
        User(self.player).update({})
        User(self.player).update({'first_name': 'foo'})
        User(self.player).update({'last_name': 'foo'})
        User(self.player).update({'email': 'a@b.c'})

        self.assertRaises(ValueError, User(self.player).update, {'email': ''})
        self.assertRaises(ValueError, User(self.player).update, {'email': 'f'})

        details_to_set = {
            'username': self.player,
            'email': 'b@c.d',
            'first_name' : 'first',
            'last_name' : 'last'
        }

        User(self.player).update(details_to_set)
        compare(User(self.player).read(), details_to_set)
