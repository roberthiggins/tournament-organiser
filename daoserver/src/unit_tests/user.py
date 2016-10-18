"""
Checking whether users are players in tournaments, admins, organisers, etc.
"""

from datetime import date, timedelta
from flask_testing import TestCase
from testfixtures import compare

from app import create_app
from models.dao.account import Account, db
from models.dao.tournament_entry import TournamentEntry as Entry
from models.user import User

from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=no-member,no-init,invalid-name,missing-docstring
class UserTests(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        self.player = 'player_1'
        today = date.today()

        db.create_all()
        self.injector = TournamentInjector()
        self.injector.inject('yesterday', date=today - timedelta(days=1),
                             past_event=True)
        self.injector.inject('today', date=today)
        self.injector.inject('tomorrow', date=today + timedelta(days=1))
        db.session.add(Account(self.player, '{}@bar.com'.format(self.player)))
        db.session.add(Entry(self.player, 'yesterday'))
        db.session.add(Entry(self.player, 'today'))
        db.session.add(Entry(self.player, 'tomorrow'))

    def tearDown(self):
        Entry.query.filter_by(player_id=self.player).delete()
        Account.query.filter_by(username=self.player).delete()
        self.injector.delete()
        db.session.remove()

    def test_get_last_tournament(self):
        compare(User(self.player).get_last_tournament().name, 'today')

    def test_get_next_tournament(self):
        compare(User(self.player).get_next_tournament().name, 'today')
