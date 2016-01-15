"""
Module to make draws for tournaments
"""

from collections import deque
from entry_db import EntryDBConnection

class RoundRobin(object):
    """
    Each entry plays each other entry.

    Assuming a list of entries, ordered by id, each entry will play the next
    entry in the list for the forst round. Each round the entry will play the
    following entry, etc.
    """

    def __init__(self, tournament_id):
        self.tournament_id = tournament_id
        self.entry_db_conn = EntryDBConnection()

    def draw(self, round_to_draw):
        """
        Make the draw for a round.
        This writes the draw to the db.

        Returns: The draw for convenience.
        """
        entry_list = deque(self.entry_db_conn.entry_list(self.tournament_id))
        entry_list.rotate(round_to_draw - 1)
        return self.determine_matchup(list(entry_list), [])

    def determine_matchup(self, singles, pairs):
        """
        Determine a single match up for a round robin tournie
        Algorithm:
            - The first and last in the list play each other.
            - The person in the middle is the bye, if they exist
            - The list should be rotated in subsequent rounds.
        Expects:
            - singles is a list of all singles yet to be pairs
            - pairs is a list of pairings:
                ({entry from singles} or 'BYE', {entry from singles} or 'BYE')
        """
        if len(singles) == 0:
            return pairs
        elif len(singles) == 1:
            pairs.append((singles[0], 'BYE'))
            return pairs
        else:
            pairs.append((singles[0], singles[-1]))
            return self.determine_matchup(singles[1:-1], pairs)
