"""
Ranking Strategies

Tournaments will have a way to order their players based on the scores they
have. This will vary from tournament to tournament.

The default here is RankingStrategy. It is the null strategy so it will just
return lists in the order they were handed in and will pick the first db entry
as the winner of any given category.
"""
from entry_db import EntryDBConnection

class RankingStrategy(object):
    """
    A default RankingStrategy will return a list of entries in the order they
    are output from the db.
    """

    def __init__(self, tournament_id, score_categories_func):
        self.tournament_id = tournament_id
        self.entry_db_conn = EntryDBConnection()
        self.score_categories = score_categories_func

    def total_score(self, scores):
        """
        Calculate the total score for the entry
        """

        categories = self.score_categories()
        for cat in categories:
            agg_score = sum(
                [x['score'] for x in scores if x['category'] == cat['id']])
            agg_total = sum(
                [x['max_val'] for x in scores if x['category'] == cat['id']])
            cat['total_score'] = \
                float(agg_score) / float(agg_total) * int(cat['percentage'])

        return sum([x['total_score'] for x in categories])

    def overall_ranking(self, error_on_incomplete=False): # pylint: disable=W0613
        """
        Combines all scores for an overall ranking of entries.

        error_on_incomplete: when true this will raise a RuntimeError if any
            of the entrants have incopmlete scores.
        """
        entries = self.entry_db_conn.entry_list(self.tournament_id)
        for i, entry in enumerate(entries):
            entry['total_score'] = self.total_score(entry['scores'])
            entry['ranking'] = i + 1
        return entries

    def ranking_by_category(self, category):
        """Rank entries based on a specific score only"""
        if not category:
            return self.overall_ranking()
        return self.overall_ranking()
