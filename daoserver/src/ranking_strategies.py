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

    def __init__(self, tournament_id):
        self.tournament_id = tournament_id
        self.entry_db_conn = EntryDBConnection()

    def overall_ranking(self, error_on_incomplete=False):
        """
        Combines all scores for an overall ranking of entries.
        
        error_on_incomplete: when true this will raise a RuntimeError if any
            of the entrants have incopmlete scores.
        """
        entries = self.entry_db_conn.entry_list(self.tournament_id)
        return entries

    def ranking_by_category(self, category):
        return self.overall_ranking()
