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

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import and_

from models.tournament import Tournament

db = SQLAlchemy()

class ScoreCategory(db.Model):
    """ A row from the score_category table"""
    __tablename__ = 'score_category'
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.String(50),
                              db.ForeignKey(Tournament.name))
    display_name = db.Column(db.String(50), nullable=False)
    percentage = db.Column(db.Integer, nullable=False, default=100)

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

