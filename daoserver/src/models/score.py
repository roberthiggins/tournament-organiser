"""
ORM module for a score an entry can get in a game

Scores for tournaments are set up thusly:
    - a tournament will have some score_categories (battle, etc.)
    - an individual entry can get scores.
    - a score key is an instance of a score_category for a given round
TODO:
    - the relationship here could be tidied up somewhat.

"""
# pylint: disable=C0103

from sqlalchemy.sql.expression import and_

from models.db_connection import db
from models.tournament import Tournament
from models.tournament_round import TournamentRound

class ScoreCategory(db.Model):
    """ A row from the score_category table"""
    __tablename__ = 'score_category'
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.String(50),
                              db.ForeignKey(Tournament.name),
                              nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    percentage = db.Column(db.Integer, nullable=False, default=100)
    tournament = db.relationship(Tournament)

    def __init__(self, tournament_id, display_name, percentage):
        self.tournament_id = tournament_id
        self.display_name = display_name
        try:
            percentage = int(percentage)
        except ValueError:
            raise ValueError('percentage must be an integer')
        self.percentage = int(percentage)

    def __repr__(self):
        return '<ScoreCategory ({}, {}, {})>'.format(
            self.tournament_id,
            self.display_name,
            self.percentage)

    def write(self):
        """To the DB"""

        # All the score percantages can only sum to 100 or less.
        existing = ScoreCategory.query.\
            filter_by(tournament_id=self.tournament_id).all()
        if (sum([x.percentage for x in existing]) + self.percentage) > 100:
            raise ValueError('percentage too high: {}'.format(self))

        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

class ScoreKey(db.Model):
    """A row in the score_key table"""

    __tablename__ = 'score_key'
    id = db.Column(db.Integer, db.Sequence('score_key_id_seq'), unique=True)
    key = db.Column(db.String(50), primary_key=True)
    min_val = db.Column(db.Integer)
    max_val = db.Column(db.Integer)
    category = db.Column(db.Integer,
                         db.ForeignKey(ScoreCategory.id),
                         primary_key=True)
    score_category = db.relationship(ScoreCategory)

    def __init__(self, key, category, min_val, max_val):
        self.key = key
        self.category = category

        try:
            self.min_val = int(min_val)
        except ValueError:
            raise ValueError('Minimum Score must be an integer')

        try:
            self.max_val = int(max_val)
        except ValueError:
            raise ValueError('Maximum Score must be an integer')

    def __repr__(self):
        return '<ScoreKey ({}, {}, {}, {}, {})>'.format(
            self.id,
            self.key,
            self.category,
            self.min_val,
            self.max_val)

    def write(self):
        """To the DB"""

        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception('Score already set')

class RoundScore(db.Model):
    """A score for an entry in a round"""

    __tablename__ = 'round_score'
    score_key_id = db.Column(db.Integer,
                             db.ForeignKey(ScoreKey.id),
                             primary_key=True)
    round_id = db.Column(db.Integer,
                         db.ForeignKey(TournamentRound.id),
                         primary_key=True)
    score_key = db.relationship(ScoreKey)
    round = db.relationship(TournamentRound)

    def __init__(self, score_key, round_id):
        self.score_key_id = score_key
        self.round_id = int(round_id)

    def __repr__(self):
        return '<RoundScore ({}, {})>'.format(self.score_key_id, self.round_id)

    def write(self):
        """To the DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise