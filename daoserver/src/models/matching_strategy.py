"""
Module to make draws for tournaments
"""

from collections import deque
import itertools

class MatchingStrategy(object):
    """
    Strategy pattern for matching entries into games
    """

    draw_for_all_rounds = False

    def match(self, entry_list):
        """Do the draw"""
        raise NotImplementedError()

class RoundRobin(MatchingStrategy):
    """
    Each entry plays each other entry.

    Assuming a list of entries, ordered by id, each entry will play the next
    entry in the list for the forst round. Each round the entry will play the
    following entry, etc.
    """

    draw_for_all_rounds = True
    round_to_draw = 1

    def set_round(self, round_num):
        """Set the round to draw"""
        self.round_to_draw = int(round_num)
        return self

    def match(self, entry_list):
        """
        Match the entrants into pairs.

        Returns: A list of Tuples - each is a pair of entrants.
        """
        entry_list = deque(entry_list)
        entry_list.rotate(self.round_to_draw - 1)
        return self._determine_matchup(list(entry_list), [])

    def _determine_matchup(self, singles, pairs):
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
            return self._determine_matchup(singles[1:-1], pairs)


class SwissChess(MatchingStrategy):
    """
    Entries are ranked and paired off.

    Each potential draw is checked for the difference in points. The
    permutation with the lowest difference is used.

    Players cannot play each other more than once
    No BYEs are allowed currently
    """

    def __init__(self, **args):
        super(SwissChess, self)
        self.rank_func = args.get('rank')
        self.re_match = args.get('re_match')

    # pylint: disable=unused-argument
    def set_round(self, round_num):
        """We don't care what the round is"""
        return self

    def match(self, entry_list):
        """
        Match the entrants into pairs.

        Algorithm:
            - All permutations of the player base are made
            - All pairs are checked for repeat matchups
                - a repeat discards the entire draw
            - The difference in points is calculated for each pair
            - The permutation with the lowest total difference is chosen

        Returns: A list of Tuples - each is a pair of entrants.
        """
        entry_list = [{
            'match_score': self.rank_func(x),
            'name': x.player_id,
            'entry': x
            } for x in entry_list]
        if len(entry_list) % 2 == 1:
            entry_list.append({'match_score': 0, 'name': 'BYE', 'entry': 'BYE'})

        possible_games = itertools.combinations(entry_list, 2)

        possible_games = [x for x in possible_games if not self.re_match(x)]
        if len(possible_games) == 0:
            return []

        possible_games = [x + \
            (abs(int(x[0]['match_score']) - int(x[1]['match_score']))**2,) \
            for x in possible_games]
        possible_draws = itertools.combinations(possible_games,
                                                len(entry_list) / 2)

        legal_draws = [x for x in possible_draws if self._check_legal_draw(x)]
        best_draw = sorted(legal_draws, cmp=lambda x, y: \
            cmp(sum([i[2] for i in x]), sum([i[2] for i in y])))[0]

        return [(game[0]['entry'], game[1]['entry']) for game in best_draw]

    def pair_entries(self, singles, pairs):
        """
        Build a list of pairs from a list of entries.
        """
        if len(singles) == 0:
            return pairs
        elif len(singles) == 1:
            pairs.append((singles[0]))
            return pairs
        else:
            pairs.append((singles[0], singles[1]))
            return self.pair_entries(singles[2:], pairs)

    @staticmethod
    def _check_legal_draw(draw):
        """set of all players should equal num_games *2"""
        ids = set([x[0]['name'] for x in draw])
        ids = ids.union(set([x[1]['name'] for x in draw]))
        return len(ids) == len(draw) * 2
