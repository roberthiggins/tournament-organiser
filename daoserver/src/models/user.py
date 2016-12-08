"""
Model of a user
"""

import datetime
import re
from sqlalchemy.sql.expression import and_

from models.authentication import check_auth
from models.dao.account import db, Account, AccountSecurity
from models.dao.tournament import Tournament as TournDAO
from models.dao.tournament_entry import TournamentEntry
from models.permissions import PERMISSIONS
from models.tournament import all_tournaments_with_permission, Tournament

# pylint: disable=no-member

def must_exist_in_db(func):
    """ A decorator that requires the tournament exists in the db"""
    def wrapped(self, *args, **kwargs): # pylint: disable=missing-docstring
        if not self.exists_in_db:
            print 'Cannot find user {}'.format(self.username)
            raise ValueError('Cannot find user {}'.format(self.username))
        return func(self, *args, **kwargs)
    return wrapped

def strip_none(array):
    """Strip all elements that are None"""
    return [x for x in array if x is not None]

class User(object):
    """A User"""

    def __init__(self, username):
        self.username = username
        self.exists_in_db = self.get_dao() is not None

    def get_dao(self):
        """Convenience method to recover DAO"""
        return Account.query.filter_by(username=self.username).first()

    def create(self, details):
        """Add an account"""
        email = details['email']
        password1 = details['password1']
        password2 = details['password2']
        first_name = details.get('first_name', None)
        last_name = details.get('last_name', None)

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError('This email does not appear valid')

        if password1 != password2 or not password1:
            raise ValueError('Please enter two matching passwords')

        if self.exists_in_db:
            raise ValueError('A user with the username {} already exists! ' \
                'Please choose another name'.format(self.username))

        db.session.add(
            Account(self.username, email, first_name, last_name))
        db.session.add(AccountSecurity(self.username, password1))
        db.session.commit()

        self.exists_in_db = True

    @must_exist_in_db
    def read(self):
        """ username and email for contact and identification"""
        return {
            'username': self.username,
            'email': self.get_dao().contact_email,
            'first_name' : self.get_dao().first_name,
            'last_name' : self.get_dao().last_name,
        }

    @must_exist_in_db
    def update(self, details):
        """Update user details"""

        dao = self.get_dao()
        email = details.get('email', dao.contact_email)
        first_name = details.get('first_name', dao.first_name)
        last_name = details.get('last_name', dao.last_name)

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError('This email does not appear valid')

        dao.contact_email = email
        dao.first_name = first_name
        dao.last_name = last_name

        db.session.add(dao)
        db.session.commit()

    @must_exist_in_db
    def available_actions(self):
        """
        Returns a list of actions the user can perform
        Format:
            [
                {
                    'title': 'Things to do in Summer'
                    items: [
                        {
                            'action': 'register',
                            'text': 'Go skiing',
                            'tournament': (optional) 'some_event',
                            'username': (optional) 'self.username',
                            'round': (optional) 1
                        },
                        {'action': 'nextgame', 'text': 'Next snowball fight'}
                    ]
                }
            ]
        """
        categories = [
            self.get_play_actions(),
            self.get_account_actions(),
            self.get_organiser_actions(),
            self.get_feedback_actions()
        ]

        return [x for x in strip_none(categories) if len(x['actions']) > 0]

    # pylint: disable=too-many-arguments
    def action(self, text, act, username=False, tourn=None, rnd=None):
        """Make a dict containing action info ready for outside consumers"""
        base_obj = {
            'text': text,
            'action': act
        }
        if username:
            base_obj['username'] = self.username
        if tourn is not None:
            base_obj['tournament'] = tourn
        if rnd is not None:
            base_obj['round'] = rnd

        return base_obj

    def get_feedback_actions(self):
        """Get the admin actions the user can perform"""
        return {
            'title': 'Feedback',
            'actions': [self.action('Place Feedback', 'place_feedback')]
        }
        # self.action('about players', 'player_info'),
        # self.action('about to', 'to_info'),
        # self.action('about tournie', 'tournament_info'),
        # self.action('Update my player details', 'update_details', True)

    @must_exist_in_db
    def get_display_name(self):
        """Get the real name of the user"""
        full_name = '{} {}'.format(self.get_dao().first_name,
                                   self.get_dao().last_name).strip()
        return full_name if full_name is not '' else self.username

    def get_account_actions(self):
        """Basic user actions for viewing and entering tournaments"""

        return {
            'title': 'Account',
            'actions': strip_none([
                self.action('See your user details', 'user_details', True),
                self.action('Logout', 'logout'),
            ])
        }
        # Get applications to update
        # self.action('Update application', 'update_application'),
        # Get applications
        # self.action('See application status', 'update_application'),
        # Upcoming tournaments
        # self.action('See upcoming tournaments for user user_1',
        #             'upcoming_tournaments', True)

    def get_last_tournament(self):
        """The last tournament for the user"""
        return TournDAO.query.join(TournamentEntry).filter(and_(
            TournamentEntry.player_id == self.username,
            TournDAO.date <= datetime.date.today()
        )).order_by(TournDAO.date.desc()).first()

    def get_next_tournament(self):
        """The next tournament for the user"""
        return TournDAO.query.join(TournamentEntry).filter(and_(
            TournamentEntry.player_id == self.username,
            TournDAO.date >= datetime.date.today()
        )).order_by(TournDAO.date.asc()).first()

    def get_organiser_actions(self):
        """Get all the actions the user can perform as a TO"""

        # Find all tournaments that can have their rounds set
        modifiable_tournaments = all_tournaments_with_permission(
            PERMISSIONS.get('MODIFY_TOURNAMENT'),
            self.username)
        set_rounds = [
            self.action('Set num rounds for {}'.format(x), 'set_rounds',
                        tourn=x) for x in modifiable_tournaments]

        # Find all tournaments that can have their missions set
        set_mission_actions = [
            self.action('Set missions for {}'.format(x), 'set_missions',
                        tourn=x) for x in modifiable_tournaments]

        # Find all tournaments that can have their score_categories set
        set_cats = [
            self.action('Set scoring categories for {}'.format(x),
                        'set_score_categories', tourn=x) \
            for x in modifiable_tournaments]

        actions = [self.action('Create a Tournament', 'create_tournament')] \
            + set_rounds + set_cats + set_mission_actions

        return {
            'title': 'Organise',
            'actions': strip_none(actions)
        }

    def get_play_actions(self):
        """Get all the actions for playing in tournaments"""

        last_t = self.get_last_tournament()
        next_t = self.get_next_tournament()
        next_game = self.action('Get next game', 'next_game', \
            tourn=next_t.name) if next_t is not None else None
        tourn_rounds = [x for x in \
                range(1, Tournament(next_t.name).get_dao().rounds.count())]\
            if next_t is not None else []

        draws = [
            self.action('Get the draw for {} round {}'.format(next_t.name, x),
                        'get_draw', tourn=next_t.name, rnd=x) \
            for x in tourn_rounds]

        submits = [
            self.action('See upcoming tournaments', 'tournament_list'),
            {'text': 'Submit a tournament score for {}'.format(next_t.name),
             'action': 'enter_tournament_score',
             'tournament': next_t.name,
             'username': self.username} if next_t is not None else None,
            {'text': 'Submit a game score for {}'.format(next_t.name),
             'action': 'enter_game_score',
             'tournament': next_t.name,
             'username': self.username} if next_t is not None else None,
            {'text': 'See total scores for {}'.format(last_t.name),
             'action': 'get_rankings',
             'tournament': last_t.name} if last_t is not None else None,
        ]
        # Table layout
        # self.action('Get the table layout', 'table_layout'),
        # Opponent army list
        # self.action('Get an opponent army list', 'get_opponent'),
        # Time remaining
        # self.action('Get the time remaining in the round', 'get_clock'),
        # Previous games
        # self.action('Review previous games', 'see_previous_games')

        return {
            'title': 'Play',
            'actions': strip_none([next_game] + draws + submits)
        }

    def login(self, password):
        """Log the user in"""
        if Account.query.filter_by(username=self.username).first() is None or \
        not check_auth(self.username, password):
            raise ValueError('Username or password incorrect')
