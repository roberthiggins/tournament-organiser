"""
Model of a tournament

This serves two functions.
    - It houses tournament functions to reduce complexity in the app class
    - It holds a tournament object for housing of scoring strategies, etc.
"""

from tournament_db import TournamentDBConnection


class Tournament(object):
    """A tournament DAO"""

    def __init__(self, tournament_id=None):
        self.tourn_db_conn = TournamentDBConnection()
        self.tournament_id = tournament_id
        self.exists_in_db = tournament_id is not None \
            and self.tourn_db_conn.tournament_exists(tournament_id)

    def details(self):
        """
        Get details about a tournament. This includes entrants and format
        information
        """
        #TODO pythonesque
        if not self.exists_in_db:
            raise RuntimeError(
                'No information is available on {} '.format(
                    self.tournament_id))

        details = self.tourn_db_conn.tournament_details(self.tournament_id)

        return {
            'name': details[1],
            'date': details[2],
            'details': {
                'rounds': details[3] if details[3] is not None else 'N/A',
                'score_format': details[4] if details[4] is not None else 'N/A',
            }
        }

