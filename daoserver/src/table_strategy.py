"""
Module to contain table allocation strategy
"""

import itertools

class LayoutProtest(object):
    """
    A count of the protests for a proposed draw.
    The default is suitable for a 2-player-per-game draw. It contains:
        - 0_protests - count of games for where neither entry protested
        - 1_protests - count of games for where 1 entry protested
        - 2_protests - count of games for where both entries protested
    """
    def __init__(self):
        self.protests = [0, 0, 0]

    def total_protests(self):
        """ Sum of all protests """
        return sum(self.protests[1:])

    def __repr__(self):
        rep = [x for x in self.protests]
        rep.append(self.total_protests())
        return '[' + ','.join(str(e) for e in rep) + ']'

class ProtestAvoidanceStrategy(object):
    """
    Allocate tables by determining all possible options and allocating based on
    fewest protests.

    Algorithm:
        Protest:
            - Assume a game has two entrants (who have a history of tables
            played on)
            - When a table is proposed one, or both, entrants may protest
            - This gives a protest score of 0, 1, 2 (no-protest -> both protest)
        Layout:
            - A layout is a single possible configuration of entrants on
            tables. Essentially this is one candidate for final configuration.
        Allocation:
            - For all possible layouts, determine the aggregate protest
            - The least protested layout is chosen
        Variations:
            - There are four obvious variations:
                - Avoid double protests - Least Outrage
                - Avoid single protests - split happy and sad (perhaps good for
                the competitive tables where playing there before-hand is a
                real advantage)
                - Avoid no protests - least variety
                - Lowest aggregate protest - Utility happiness
        Time-complexity:
            - n3 for n games
        Memory Complexity:
            - 4 * n3 integers for n games.
        Potential Trade-off:
            A reasonably complex select to get table history for each player
            could be stored with the entry.
    """

    @staticmethod
    def get_protest_score_for_game(table, entries):
        """
        Get the protest score for a single game.
        Returns a single protest score between 0 and len(entries)
        Expects:
            - an int for the table number
            - A list of Entry
        """
        protests = 0
        table = int(table)
        for entry in entries:
            if table in entry.game_history:
                protests += 1
        return protests

    @staticmethod
    def get_protest_score_for_layout(layout):
        """
        Get the protest scores for a single layout

        Expects:
            List of tuples [(table, [entries at that table])]
            Note that the game might simply be the string 'BYE'
        Returns:
            A LayoutProtest
        """
        if len(layout) == 0:
            return LayoutProtest()
        num_entries = len(layout[0][1])
        if any(len(x[1]) != num_entries for x in layout):
            raise IndexError('Some games have differing numbers of entries')

        protest = LayoutProtest()
        for game in layout:
            game_1 = game[1][0]
            game_2 = game[1][1]

            try:
                protest_score = \
                    ProtestAvoidanceStrategy.get_protest_score_for_game(
                        game[0], (game_1, game_2))
            except AttributeError:
                protest_score = 0
            protest.protests[protest_score] += 1

        return protest

    # pylint: disable=R0201
    def determine_tables(self, drawn_games):
        """
        The main method that returns a table configuration.

        Assumptions:
            Each Entry is expected to have a correct playing history as this
            will be used for determining the draw.
        Expects:
            A list of games. Each game should be a tuple of 2 Entry

        Returns:
            A list of tuples with table number prepended to each. e.g.
            [(1, Entry, Entry), (2, Entry, Entry)]
        """
        permutations = list(itertools.permutations(drawn_games))
        permutations = [[(i+1, [e['entry_1'], e['entry_2']]) \
            for i, e in enumerate(x)] for x in permutations]

        protests = [
            (ProtestAvoidanceStrategy.get_protest_score_for_layout(x), x) \
            for x in permutations
        ]

        protests.sort(cmp=lambda x, y: cmp(
            x[0].total_protests(),
            y[0].total_protests()))

        return protests[0][1]
