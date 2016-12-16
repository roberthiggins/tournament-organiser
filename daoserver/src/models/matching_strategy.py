"""
Module to make draws for tournaments
"""

from collections import deque

class RoundRobin(object):
    """
    Each entry plays each other entry.

    Assuming a list of entries, ordered by id, each entry will play the next
    entry in the list for the forst round. Each round the entry will play the
    following entry, etc.
    """

    DRAW_FOR_ALL_ROUNDS = True

    def match(self, round_to_draw, entry_list):
        """
        Match the entrants into pairs.

        Returns: A list of Tuples - each is a pair of entrants.
        """
        entry_list = deque(entry_list)
        entry_list.rotate(round_to_draw - 1)
        return self.determine_matchup(list(entry_list), [])

    def determine_matchup(self, singles, pairs):
        """
        Determine match ups for a round robin tournie
        Algorithm:
            - The first and last in the list play each other.
            - The person in the middle is the bye, if they exist
            - The list should be rotated in subsequent rounds.
        Expects:
            - singles is a list of all singles yet to be pairs
            - pairs is a list of pairings:
                ({entry from singles} or 'BYE', {entry from singles} or 'BYE')
        Returns:
            - A list of Tuples of entry_db.Entry from singles
        """
        if len(singles) == 0:
            return pairs
        elif len(singles) == 1:
            pairs.append((singles[0], 'BYE'))
            return pairs
        else:
            pairs.append((singles[0], singles[-1]))
            return self.determine_matchup(singles[1:-1], pairs)
