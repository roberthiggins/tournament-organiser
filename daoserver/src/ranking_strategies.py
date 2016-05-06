"""
Ranking Strategies

Tournaments will have a way to order their players based on the scores they
have. This will vary from tournament to tournament.

The default here is RankingStrategy. It is the null strategy so it will just
return lists in the order they were handed in and will pick the first db entry
as the winner of any given category.
"""

class RankingStrategy(object):
    """
    A default RankingStrategy will return a list of entries in the order they
    are output from the db.
    """

    def __init__(self, tournament_id, score_categories_func):
        self.tournament_id = tournament_id
        self.score_categories = score_categories_func

    def total_score(self, entry):
        """
        Calculate the total score for the entry
        entry should be a TournamentEntry
        """

        categories = self.score_categories()
        scores = entry.scores
        for cat in categories:
            agg_score = sum(
                [x.value for x in scores \
                if x.score_key.score_category.display_name == cat['name'] \
                and x.value is not None])
            agg_total = sum(
                [x.score_key.max_val for x in scores \
                if x.score_key.score_category.display_name == cat['name']])
            try:
                agg_score = float(agg_score)
                agg_total = float(agg_total)
                percentage = int(cat['percentage'])
                cat['total_score'] = agg_score / agg_total * percentage
            except ZeroDivisionError:
                cat['total_score'] = 0

        return sum([x['total_score'] for x in categories])

    def overall_ranking(self, entries, error_on_incomplete=False): # pylint: disable=W0613
        """
        Combines all scores for an overall ranking of entries.

        error_on_incomplete: when true this will raise a RuntimeError if any
            of the entrants have incopmlete scores.
        """
        for i, entry in enumerate(entries):
            entry.total_score = self.total_score(entry)
            entry.ranking = i + 1
        return entries
