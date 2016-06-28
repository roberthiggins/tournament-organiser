"""
ORM module for a score an entry can get in a game

Scores for tournaments are set up thusly:
    - a tournament will have some score_categories (battle, etc.)
    - an individual entry can get scores.
    - a score key is an instance of a score_category for a given round
TODO:
    - the relationship here could be tidied up somewhat.

"""
# pylint: disable=invalid-name,no-member,too-many-arguments

from sqlalchemy.sql.expression import and_

from models.db_connection import db
from models.tournament import Tournament
from models.tournament_entry import TournamentEntry
from models.tournament_game import TournamentGame

class ScoreCategory(db.Model):
    """ A row from the score_category table"""
    __tablename__ = 'score_category'
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.String(50),
                              db.ForeignKey(Tournament.name),
                              nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    min_val = db.Column(db.Integer)
    max_val = db.Column(db.Integer)
    per_tournament = db.Column(db.Boolean, nullable=False, default=False)
    percentage = db.Column(db.Integer, nullable=False, default=100)
    tournament = db.relationship(Tournament, backref=db.backref(
        'score_categories', lazy='dynamic'))

    def __init__(self, tournament_id, display_name, percentage, per_tourn,
                 min_val, max_val):
        self.tournament_id = tournament_id
        self.display_name = display_name
        self.per_tournament = per_tourn

        try:
            self.min_val = int(min_val)
            self.max_val = int(max_val)
        except ValueError:
            raise ValueError('Min and Max Scores must be integers')
        except TypeError:
            raise ValueError('Min and Max Scores must be integers')
        if self.max_val <= 0:
            raise ValueError("Max Score must be positive")
        if self.min_val < 0:
            raise ValueError("Min Score cannot be negative")
        if self.min_val > self.max_val:
            raise ValueError("Min Score must be less than Max Score")

        try:
            self.percentage = int(percentage)
            if self.percentage <= 0 or self.percentage > 100:
                raise TypeError()
        except TypeError:
            raise ValueError("Percentage must be between 1 and 100")

    def __repr__(self):
        return '<ScoreCategory ({}, {}, {}, {}, {}, {})>'.format(
            self.tournament_id,
            self.display_name,
            self.percentage,
            self.per_tournament,
            self.min_val,
            self.max_val)

    def clashes(self):
        """
        Check that the ScoreCategory will work in the proposed tournament. This
        means that the total score percentage for all categories in the
        tournament won't exceed 100%
        """
        existing = ScoreCategory.query.\
            filter(and_(ScoreCategory.tournament_id == self.tournament_id,
                        ScoreCategory.display_name != self.display_name)).all()

        if (sum([x.percentage for x in existing]) + self.percentage) > 100:
            raise ValueError('percentage too high: {}'.format(self))

        return False

class Score(db.Model):
    """An individual score tied to a ScoreCategory"""

    __tablenamene__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey(TournamentEntry.id))
    score_category_id = db.Column(db.Integer, db.ForeignKey(ScoreCategory.id))
    value = db.Column(db.Integer)

    entry = db.relationship(TournamentEntry, backref='scores')
    score_category = db.relationship(ScoreCategory, \
        backref=db.backref('scores', lazy='dynamic'))

    def __init__(self, entry_id, score_category_id, value=None):
        self.entry_id = entry_id
        self.score_category_id = score_category_id
        self.value = value

    def __repr__(self):
        return '<Score ({}, {}, {}, {})>'.format(
            self.id,
            self.entry_id,
            self.score_category_id,
            self.value)

class GameScore(db.Model):
    """A Score entered in a game"""
    __tablename__ = 'game_score'
    entry_id = db.Column(db.Integer, db.ForeignKey(TournamentEntry.id),
                         primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(TournamentGame.id),
                        primary_key=True)
    score_id = db.Column(db.Integer, db.ForeignKey(Score.id),
                         primary_key=True)


    entry = db.relationship(TournamentEntry,
                            backref=db.backref('game_scores', lazy='dynamic'))
    game = db.relationship(TournamentGame,
                           backref=db.backref('game_scores', lazy='dynamic'))
    score = db.relationship(Score,
                            backref=db.backref('game_scores', lazy='dynamic'))

    def __init__(self, entry_id, game_id, score_id):
        self.entry_id = entry_id
        self.game_id = game_id
        self.score_id = score_id

    def __repr__(self):
        return '<GameScore (entry: {}, game: {}, score_id:{})>'.format(
            self.entry_id,
            self.game_id,
            self.score_id)

class TournamentScore(db.Model):
    """A one-off score for a tournament"""
    __tablename__ = 'tournament_score'
    entry_id = db.Column(db.Integer, db.ForeignKey(TournamentEntry.id),
                         primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey(Tournament.id),
                              primary_key=True)
    score_id = db.Column(db.Integer, db.ForeignKey(Score.id),
                         primary_key=True)


    entry = db.relationship(TournamentEntry, \
        backref=db.backref('tournament_scores', lazy='dynamic'))
    tournament = db.relationship(Tournament, \
        backref=db.backref('tournament_scores', lazy='dynamic'))
    score = db.relationship(Score)

    def __init__(self, entry_id, tournament_id, score_id):
        self.entry_id = entry_id
        self.tournament_id = tournament_id
        self.score_id = score_id

    def __repr__(self):
        return '<TournamentScore (entry: {}, tournament: {}, score:{})>'.format(
            self.entry_id,
            self.tournament_id,
            self.score_id)
