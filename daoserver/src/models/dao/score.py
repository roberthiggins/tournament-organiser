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

from models.dao.db_connection import db
from models.dao.tournament import Tournament
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_game import TournamentGame

# pylint: disable=too-many-instance-attributes
class ScoreCategory(db.Model):
    """ A row from the score_category table"""
    __tablename__ = 'score_category'
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.String(50),
                              db.ForeignKey(Tournament.name),
                              nullable=False)
    name = db.Column(db.String(50), nullable=False)
    min_val = db.Column(db.Integer)
    max_val = db.Column(db.Integer)
    per_tournament = db.Column(db.Boolean, nullable=False, default=False)
    percentage = db.Column(db.Integer, nullable=False, default=100)
    zero_sum = db.Column(db.Boolean, nullable=False, default=False)
    opponent_score = db.Column(db.Boolean, nullable=False, default=False)

    tournament = db.relationship(Tournament, backref=db.backref(
        'score_categories', lazy='dynamic'))

    def __init__(self, **args):
        if not args['tournament_id'] or not args['name']:
            raise ValueError('TournamentScoreCategory args missing: {}'.\
                format(args))

        self.tournament_id = args['tournament_id']
        self.per_tournament = args['per_tournament']
        self.set_name(args['name'])
        self.set_min_max(args['min_val'], args['max_val'])
        self.set_percentage(args['percentage'])
        self.zero_sum = args.get('zero_sum', False)
        self.opponent_score = args.get('opponent_score', False)

    def __repr__(self):
        return '<ScoreCategory ({}, {}, {}, {}, {}, {}, {}, {})>'.format(
            self.tournament_id,
            self.name,
            self.percentage,
            self.per_tournament,
            self.min_val,
            self.max_val,
            self.zero_sum,
            self.opponent_score)

    def clashes(self):
        """
        Check that the ScoreCategory will work in the proposed tournament. This
        means that the total score percentage for all categories in the
        tournament won't exceed 100%
        """
        existing = ScoreCategory.query.\
            filter(and_(ScoreCategory.tournament_id == self.tournament_id,
                        ScoreCategory.name != self.name)).all()

        if (sum([x.percentage for x in existing]) + self.percentage) > 100:
            raise ValueError('percentage too high: {}'.format(self))

        return False

    def set_name(self, name):
        """Set the name. It must exist"""
        if not name:
            raise ValueError('Category must have a name')
        self.name = name


    def set_percentage(self, pct):
        """Set the percentage and check it's legal"""
        try:
            self.percentage = int(pct)
            if self.percentage <= 0 or self.percentage > 100:
                raise ValueError()
        except ValueError:
            raise ValueError("Percentage must be an integer (1-100)")

    def set_min_max(self, min_val, max_val):
        """Set the min and max scores"""
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

    def update(self, **args):
        """Update an existing DAO"""
        self.tournament_id = args['tournament_id']
        self.set_name(args['name'])
        self.per_tournament = args['per_tournament']
        self.set_min_max(args['min_val'], args['max_val'])
        self.set_percentage(args['percentage'])
        self.zero_sum = args.get('zero_sum', False)
        self.opponent_score = args.get('opponent_score', False)


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
