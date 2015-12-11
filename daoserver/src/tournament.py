"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
import datetime

from draw_strategy import RoundRobin
from ranking_strategies import RankingStrategy
from tournament_db import TournamentDBConnection

def must_exist_in_db(func):
    """ A decorator that requires the tournament exists in the db"""
    def wrapped(self, *args, **kwargs):                 # pylint: disable=C0111
        if not self.exists_in_db:
            print 'Tournament not found: {}'.format(self.tournament_id)
            raise ValueError(
                'Tournament {} not found in database'.format(
                self.tournament_id))
        return func(self, *args, **kwargs)
    return wrapped

class Tournament(object):
    """A tournament DAO"""

    def __init__(self, tournament_id=None, ranking_strategy=None):
        self.tourn_db_conn = TournamentDBConnection()
        self.tournament_id = tournament_id
        self.exists_in_db = tournament_id is not None \
            and self.tourn_db_conn.tournament_exists(tournament_id)
        self.ranking_strategy = \
            ranking_strategy(tournament_id, self.list_score_categories) \
            if ranking_strategy \
            else RankingStrategy(tournament_id, self.list_score_categories)
        self.draw_strategy = RoundRobin(tournament_id)

    def add_to_db(self, date):
        """
        add a tournament
        Expects:
            - inputTournamentDate - Tournament Date. YYYY-MM-DD
        """
        if self.exists_in_db:
            raise RuntimeError('A tournament with name {} already exists! \
            Please choose another name'.format(self.tournament_id))

        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        if date.date() < datetime.date.today():
            raise ValueError('Enter a valid date')

        self.tourn_db_conn.add_tournament(
            {'name' : self.tournament_id, 'date' : date})

    @must_exist_in_db
    def create_score_category(self, category, percentage):
        """ Add a score category """
        self.tourn_db_conn.create_score_category(
            category, self.tournament_id, percentage)

    @must_exist_in_db
    def details(self):
        """
        Get details about a tournament. This includes entrants and format
        information
        """
        details = self.tourn_db_conn.tournament_details(self.tournament_id)

        return {
            'name': details[1],
            'date': details[2],
            'details': {
                'rounds': details[3] if details[3] is not None else 'N/A',
                'score_format': details[4] if details[4] is not None else 'N/A',
            }
        }

    @must_exist_in_db
    def list_score_categories(self):
        """
        List all the score categories available to this tournie and their
        percentages.
        [{ 'name': 'Painting', 'percentage': 20, 'id': 1 }]
        """
        return self.tourn_db_conn.list_score_categories(self.tournament_id)

    @staticmethod
    def list_tournaments():
        """
        GET a list of tournaments
        Returns json. The only key is 'tournaments' and the value is a list of
        tournament names
        """
        tourn_db_conn = TournamentDBConnection()
        return {'tournaments' : tourn_db_conn.list_tournaments()}

    @must_exist_in_db
    def set_score(self, key, category, min_val=0, max_val=20):
        """
        Set a score category that a player is eligible for in a tournament.

        For example, use this to specify that a tourn has a 'round_1_battle'
        score for each player.

        Expected:
            - key - unique name e.g. round_4_comp
            - (opt) min_val - for score - default 0
            - (opt) max_val - for score - default 20
        """
        if not min_val:
            min_val = 0
        if not max_val:
            max_val = 20

        self.tourn_db_conn.set_score_key(
            key=key,
            category=category,
            min_val=min_val,
            max_val=max_val)

    @must_exist_in_db
    def get_score_keys_for_round(self, round_id='next'):
        """ Get all the score keys associated with this round"""

        #TODO get next round
        if round_id == 'next':
            raise NotImplementedError('next round is unknown')

        return self.tourn_db_conn.get_score_keys_for_round(
            self.tournament_id, round_id)
