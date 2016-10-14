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

    def add_account(self, details):
        """Add an account"""
        email = details['email']
        password1 = details['password1']
        password2 = details['password2']

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError('This email does not appear valid')

        if password1 != password2 or not password1:
            raise ValueError('Please enter two matching passwords')

        if self.exists_in_db:
            raise ValueError('A user with the username {} already exists! \
                Please choose another name'.format(self.username))

        db.session.add(Account(self.username, email))
        db.session.add(AccountSecurity(self.username, password1))
        db.session.commit()

        self.exists_in_db = True

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
            self.get_entry_actions(),
            self.get_organiser_actions(),
            self.get_admin_actions()
        ]

        return [x for x in strip_none(categories) if len(x['actions']) > 0]

    def get_admin_actions(self):
        """Get the admin actions the user can perform"""
        return {
            'title': 'Administrivia',
            'actions': strip_none([
                {'text': 'Place Feedback', 'action': 'place_feedback'},
            ])
        }
        # {'text': 'about players', 'action': 'player_info'},
        # {'text': 'about to', 'action': 'to_info'},
        # {'text': 'about tournie', 'action': 'tournament_info'},
        # {'text': 'Update my player details',
        #  'action': 'update_details',
        #  'username': self.username},

    @must_exist_in_db
    def get_display_name(self):
        """Get the real name of the user"""
        return self.username

    def get_entry_actions(self):
        """Basic user actions for viewing and entering tournaments"""

        return {
            'title': 'Enter a Tournament',
            'actions': strip_none([
                {'text': 'See a list of tournaments',
                 'action': 'tournament_list'},
            ])
        }
        # Get applications to update
        # {'text': 'Update application',
        #  'action': 'update_application'},
        # Get applications
        # {'text': 'See application status',
        #  'action': 'update_application'},
        # Upcoming tournaments
        # {'text': 'See upcoming tournaments for user user_1',
        #  'action': 'upcoming_tournaments',
        #  'username': self.username},

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
        set_rounds = [{
            'text': 'Set num rounds for {}'.format(x),
            'action': 'set_rounds',
            'tournament': x
        } for x in modifiable_tournaments]

        # Find all tournaments that can have their missions set
        set_missions = [{
            'text': 'Set missions for {}'.format(x),
            'action': 'set_missions',
            'tournament': x
        } for x in modifiable_tournaments]

        # Find all tournaments that can have their score_categories set
        set_cats = [{
            'text': 'Set scoring categories for {}'.format(x),
            'action': 'set_score_categories',
            'tournament': x
        } for x in modifiable_tournaments]

        actions = \
            [{'text': 'Create a Tournament', 'action': 'create_tournament'}] \
            + set_rounds + set_cats + set_missions

        return {
            'title': 'Organise a Tournament',
            'actions': strip_none(actions)
        }

    def get_play_actions(self):
        """Get all the actions for playing in tournaments"""

        last_tourn = self.get_last_tournament()
        next_tourn = self.get_next_tournament()
        next_game = {'text': 'Get next game for {}'.format(self.username),
                     'action': 'next_game',
                     'tournament': next_tourn.name} \
            if next_tourn is not None else None
        tourn_rounds = [x for x in \
                range(1, Tournament(next_tourn.name).get_num_rounds())] \
            if next_tourn is not None else []

        draws = [{'text': 'Get the draw for {} round {}'.\
                          format(next_tourn.name, x),
                  'action': 'get_draw',
                  'tournament': next_tourn.name,
                  'round': x
                 } for x in tourn_rounds]

        return {
            'title': 'Play in a Tournament',
            'actions': strip_none([
                next_game,
                # Table layout
                # {'text': 'Get the table layout',
                #  'action': 'table_layout'},
                tuple(draws) if len(draws) > 0 else None,
                # Opponent army list
                # {'text': 'Get an opponent army list',
                #  'action': 'get_opponent'},
                # Time remaining
                # {'text': 'Get the time remaining in the round',
                #  'action': 'get_clock'},
                {'text': 'Submit a tournament score for {} entry {}'.\
                    format(next_tourn.name, self.username),
                 'action': 'enter_tournament_score',
                 'tournament': next_tourn.name,
                 'username': self.username} if next_tourn is not None else None,
                {'text': 'Submit a game score for {} entry {}'.\
                    format(next_tourn.name, self.username),
                 'action': 'enter_game_score',
                 'tournament': next_tourn.name,
                 'username': self.username} if next_tourn is not None else None,
                {'text': 'See total scores for {}'.format(last_tourn.name),
                 'action': 'get_rankings',
                 'tournament': last_tourn.name} \
                if last_tourn is not None else None,
                # Previous games
                # {'text': 'Review previous games',
                #  'action': 'see_previous_games'}
            ])
        }

    def login(self, password):
        """Log the user in"""
        if Account.query.filter_by(username=self.username).first() is None or \
        not check_auth(self.username, password):
            raise ValueError('Username or password incorrect')

    @must_exist_in_db
    def details(self):
        """ username and email for contact and identification"""
        return {'username': self.username, \
                'email': self.get_dao().contact_email}
