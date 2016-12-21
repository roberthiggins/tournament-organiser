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
                    'opponent': self.get_opponent(game),
                    'table': game.table_num,
                }
        raise ValueError("Next game not scheduled. Check with the TO.")


    def get_opponent(self, game):
        """Work out the opponent of username in the game"""
        entrants = [x.entrant.player_id for x in game.entrants \
                    if x.entrant.player_id != self.get_dao().player_id]
        return entrants[0] if len(entrants) else "BYE"

    def get_schedule(self):
        """Get the scheule of games"""
        games = [gent.game for gent in self.get_dao().game_entries]

        return [
            {
                'game_id': game.id,
                'round': game.tournament_round.ordering,
                'opponent': self.get_opponent(game),
                'table': game.table_num,
            } for game in games]

    def set_scores(self, scores):
        """
        Enter scores

        Expects a list of scores. Each should be a dict with keys:
            - game_id - The id of the game that the score is for
            - category - the category e.g. painting, round_6_battle
            - score - the score. Integer
        """

        scores = [Score(entry_id=self.get_dao().id, tournament=self.tournament,
                        score=x['score'], category=x['category'],
                        game_id=x.get('game_id', None)) for x in scores]
        for score in scores:
            score.validate()

        messages = [s.write() for s in scores]

        return messages[0] if len(messages) == 1 else '\n'.join(messages)
