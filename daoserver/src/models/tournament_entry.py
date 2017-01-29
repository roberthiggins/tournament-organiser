"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
from models.dao.account import Account
from models.dao.tournament_entry import TournamentEntry as DAO
from models.score import Score
from models.tournament import Tournament

class TournamentEntry(object):
    """An entry in a tournament"""

    def __init__(self, tournament_id, username):
        self.tournament = Tournament(tournament_id).check_exists()
        self.entry_id = self.get_entry_id(self.tournament, username)

    def get_dao(self):
        """Convenience method to recover TournamentEntry DAO"""
        # pylint: disable=no-member
        return DAO.query.filter_by(id=self.entry_id).first()

    @staticmethod
    def get_entry_id(tourn, username):
        """Get entry info from tournament and username"""

        tourn_id = tourn.tournament_id

        if not Account.username_exists(username):
            raise ValueError('Unknown player: {}'.format(username))

        try:
            # pylint: disable=no-member
            return DAO.query.\
                filter_by(tournament_id=tourn_id, player_id=username).\
                first().id
        except AttributeError:
            raise ValueError('Entry for {} in tournament {} not found'.\
                format(username, tourn_id))

    def read(self):
        """Details about a tournament entry"""
        entry = self.get_dao()
        return {
            'entry_id': entry.id,
            'username': entry.account.username,
            'tournament_name': entry.tournament.name,
        }

    def delete(self):
        """Withdraw from the tournament"""
        self.tournament.withdraw_entry(self.get_dao())

    def get_next_game(self):
        """Get the next game for given entry"""
        games = [gent.game for gent in self.get_dao().game_entries]
        games = sorted(games, key=lambda game: game.tournament_round.ordering)

        for game in games:
            if not Score.is_score_entered(game):
                return {
                    'game_id': game.id,
                    'mission': game.tournament_round.get_mission(),
                    'round': game.tournament_round.ordering,
                    'opponent': self.get_opponent_id(game),
                    'table': game.table_num,
                }
        raise ValueError("Next game not scheduled. Check with the TO.")


    def get_opponent(self, game):
        """Work out the opponent of username in the game"""
        entrants = [x.entrant for x in game.entrants \
                    if x.entrant.player_id != self.get_dao().player_id]
        return entrants[0] if len(entrants) else None

    def get_opponent_id(self, game):
        """Work out the opponent_id of username in the game"""
        opp = self.get_opponent(game)
        return opp.player_id if opp is not None else "BYE"

    def get_schedule(self):
        """Get the scheule of games"""
        games = [gent.game for gent in self.get_dao().game_entries]

        return [
            {
                'game_id': game.id,
                'round': game.tournament_round.ordering,
                'opponent': self.get_opponent_id(game),
                'table': game.table_num,
            } for game in games]

    def opp_score(self, game_score):
        """
        Returns the score or the corresponding score for the opponent if it is
        an opponent-entered score
        """
        game = game_score.game
        cat = game_score.score.score_category

        if cat.opponent_score:
            opp_scores = self.get_opponent(game).game_scores.\
                filter_by(game_id=game.id).all()
            for score in opp_scores:
                if score.score.score_category.id == cat.id:
                    return score
            return None
        return game_score

    def get_game_entered_scores(self, game_id):
        """Get the game scores for a game in dict format"""
        per_g_cats = self.get_dao().tournament.score_categories.\
            filter_by(per_tournament=False).all()
        game_scores = [self.opp_score(x) for x in self.get_dao().game_scores.\
            filter_by(game_id=game_id).all()]

        template = dict((x.name, None) for x in per_g_cats)
        template['game_id'] = game_id

        scores = dict((x.score.score_category.name, x.score.value) \
                      for x in game_scores)
        template.update(scores)
        return template

    def get_tournament_entered_scores(self):
        """Get all tournament scores in dict format"""
        per_t_cats = self.get_dao().tournament.score_categories.\
            filter_by(per_tournament=True).all()
        template = dict((x.name, None) for x in per_t_cats)

        scores = dict((x.score.score_category.name, x.score.value) \
                      for x in self.get_dao().tournament_scores.all())

        template.update(scores)
        return template

    def get_scores_entered(self):
        """
        Get the scores enterd by an entrant. Note that opponent_scored fields
        will return the opponent's score

        They will come in the format
            {
                per_tournament: {
                    painting: 15
                },
                per_game: [
                    {
                        game_id: 12345,
                        battle: 20,
                        fair play: None
                    },
                ]
            }

        """
        entries = sorted(self.get_dao().game_entries.all(),
                         key=lambda ent: ent.game.tournament_round.ordering)

        return {
            'per_tournament': self.get_tournament_entered_scores(),
            'per_game': [self.get_game_entered_scores(e.game.id) \
                for e in entries]
        }

    def set_scores(self, scores):
        """
        Enter scores

        Expects a list of scores. Each should be a dict with keys:
            - game_id - The id of the game that the score is for
            - category - the category e.g. painting, round_6_battle
            - score - the score. Integer
        """
        if scores is None or not any(scores):
            raise ValueError(Score.INVALID_SCORE.format(None))

        scores = [Score(entry_id=self.get_dao().id, tournament=self.tournament,
                        **x) for x in scores]

        for score in scores:
            score.validate()

        messages = [s.write() for s in scores]

        return messages[0] if len(messages) == 1 else '\n'.join(messages)
