"""
An entry in a tournament
"""
from flask import json

class Entry(json.JSONEncoder):
    """
    A tournament is composed of entries who play each other. This is distinct
    from users or accounts as there may be multiple players on a team, etc.
    """

    #pylint: disable=R0913
    def __init__(
            self,
            entry_id=None,
            username=None,
            tournament_id=None,
            game_history=None,
            scores=None):
        self.entry_id = entry_id
        self.username = username
        self.tournament_id = tournament_id
        self.game_history = game_history
        self.ranking = None
        self.scores = scores
        self.total_score = 0

    def __repr__(self):
        return str(self.entry_id)
