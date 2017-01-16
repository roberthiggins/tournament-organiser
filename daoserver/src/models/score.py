"""
Logic for scores goes here
"""
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.sql.expression import and_

from models.dao.db_connection import db
from models.dao.game_entry import GameEntrant
from models.dao.score import Score as DAO, ScoreCategory, TournamentScore, \
GameScore
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_game import TournamentGame

class Score(object):
    """Model for a score in a tournament or game"""

    GAME_AS_TOURN = '{} should be entered per-tournament'
    GAME_NOT_FOUND = '{} not entered. Game {} cannot be found'

    def __init__(self, **args):
        # pylint: disable=no-member
        self.score = args.get('score', None)
        self.tournament = args.get('tournament').get_dao()
        game_id = args.get('game_id', None)
        try:
            if game_id is not None:
                self.game = TournamentGame.query.filter_by(id=game_id).first()
                if self.game is None:
                    raise DataError()
            else:
                self.game = None
        except DataError:
            db.session.rollback()
            raise TypeError(self.GAME_NOT_FOUND.format(self.score, game_id))

        self.category = ScoreCategory.query.filter_by(
            tournament_id=self.tournament.name, name=args['category']).first()

        if self.category is None:
            raise TypeError('Unknown category: {}'.format(args['category']))

        if self.category.opponent_score:
            self.entry = self.game.entrants.filter(
                GameEntrant.entrant_id != args['entry_id']).first().entrant
        else:
            self.entry = TournamentEntry.query.\
                filter_by(id=args['entry_id']).first()
        if self.entry is None:
            raise ValueError('Unknown entrant: {}'.format(args['entry_id']))


    def get_dao(self):
        """Convenience method to recover TournamentDAO"""
        # pylint: disable=no-member
        if self.category.per_tournament:
            return TournamentScore.query.join(DAO).join(ScoreCategory).filter(
                and_(TournamentScore.entry_id == self.entry.id,
                     TournamentScore.tournament_id == self.tournament.id,
                     ScoreCategory.id == self.category.id)).first()

        return GameScore.query.join(DAO).filter(
            and_(GameScore.entry_id == self.entry.id,
                 GameScore.game_id == self.game.id,
                 DAO.score_category_id == self.category.id)).first()


    @staticmethod
    def is_score_entered(game_dao):
        """
        Determine if all the scores have been entered for this game.
        Not that, if false, the result will be double checked and possibly
        updated
        """
        if game_dao is not None and game_dao.score_entered:
            return True

        per_game_scores = len(game_dao.tournament_round.tournament.\
            score_categories.filter_by(per_tournament=False).all())
        if per_game_scores <= 0:
            raise AttributeError(
                '{} does not have any scores associated with it'.\
                format(game_dao.tournament_round.tournament.name))

        scores_expected = per_game_scores * len(game_dao.entrants.all())

        if len(game_dao.game_scores.all()) == scores_expected:
            game_dao.score_entered = True
            db.session.add(game_dao)
            db.session.commit()
            return True

        return False


    def validate(self):
        """Validate an entered score. Returns True or raises Exception"""
        invalid_score = ValueError('Invalid score: {}'.format(self.score))

        try:
            score = int(self.score)
        except TypeError:
            raise invalid_score

        if score < self.category.min_val or score > self.category.max_val:
            raise invalid_score

        if self.game is None and not self.category.per_tournament:
            raise TypeError(self.GAME_AS_TOURN.format(self.category.name))

        if self.game is not None and self.category.per_tournament:
            raise TypeError('Cannot enter a per-tournament score '\
                '({}) for a game (id: {})'.\
                format(self.category.name, self.game.id))

        # If zero sum we need to check the score entered by the opponent
        if self.game is not None and self.category.zero_sum:
            # pylint: disable=no-member
            game_scores = GameScore.query.join(DAO, ScoreCategory).\
                    filter(and_(GameScore.game_id == self.game.id,
                                ScoreCategory.name == self.category.name,
                                GameScore.entry_id != self.entry.id)).all()
            existing_score = sum([x.score.value for x in game_scores])
            if existing_score + score > self.category.max_val:
                raise invalid_score


    def write(self):
        """
        Enters a score for category into tournament for player.

        Expects: score - integer
        """
        self.validate()
        if self.get_dao() is not None:
            raise ValueError('{} not entered. Score is already set'.\
                format(self.score))

        try:
            score_dao = DAO(self.entry.id, self.category.id, self.score)
            db.session.add(score_dao)
            db.session.flush()

            if self.game is not None:
                db.session.add(
                    GameScore(self.entry.id, self.game.id, score_dao.id))
            else:
                db.session.add(TournamentScore(self.entry.id, \
                    self.tournament.id, score_dao.id))
            db.session.commit()
        except IntegrityError as err:
            db.session.rollback()
            if 'is not present in table "entry"' in err.__repr__():
                raise AttributeError('{} not entered. Entry {} doesn\'t exist'.\
                    format(self.score, self.entry.id))
            raise err

        return 'Score entered for {}: {}'.\
            format(self.entry.player_id, self.score)
