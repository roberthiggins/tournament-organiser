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
        """ Sum of all protests. A double protest counts as two individuals."""
        return self.protests[1] + self.protests[2] * 2

    def __repr__(self):
        rep = [x for x in self.protests]
        rep.append(self.total_protests())
        return '[' + ','.join(str(e) for e in rep) + ']'

class Table(object):
    """
    A game table. It contains one or more entrants and a table number
    """
    def __init__(self, table_number=0, entrants=None):
        self.table_number = int(table_number)
        self.entrants = entrants

    def protest_score(self):
        """
        Get the protest score for a single game.
        Returns a single protest score between 0 and len(entries)
        """
        protests = 0
        try:
            for entry in self.entrants:
                if self.table_number in entry.game_history:
                    protests += 1
        except AttributeError:
            pass

        return protests

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
    def get_protest_score_for_layout(layout):
        """
        Get the protest scores for a single layout

        Expects:
            List of Table
            Note that the game might simply be the string 'BYE'
        Returns:
            A LayoutProtest
        """
        if len(layout) == 0:
            return LayoutProtest()

        num_entries = len(layout[0].entrants)
        if any(len(x.entrants) != num_entries for x in layout):
            raise IndexError('Some games have differing numbers of entries')

        protest = LayoutProtest()
        for game in layout:
            protest.protests[game.protest_score()] += 1

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
            A list of Table
        """
        permutations = list(itertools.permutations(drawn_games))
        permutations = [
            [Table(i+1, list(e)) for i, e in enumerate(x)] \
            for x in permutations]

        protests = [
            (ProtestAvoidanceStrategy.get_protest_score_for_layout(x), x) \
            for x in permutations
        ]

        protests.sort(cmp=lambda x, y: cmp(
            x[0].total_protests(),
            y[0].total_protests()))

        return protests[0][1]
