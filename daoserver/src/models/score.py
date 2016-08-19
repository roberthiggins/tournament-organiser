"""
Logic for scores goes here
"""
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.sql.expression import and_

from models.dao.db_connection import db
from models.dao.score import Score, ScoreCategory, TournamentScore, \
GameScore

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
            format(game_dao))

    scores_expected = per_game_scores * len(game_dao.entrants.all())

    if len(game_dao.game_scores.all()) == scores_expected:
        game_dao.score_entered = True
        db.session.add(game_dao)
        db.session.commit()
        return True

    return False


def upsert_tourn_score_cat(tournament_id, cat):
    """
    Upsert a tournament score category to the DB
    """
    # pylint: disable=no-member
    dao = ScoreCategory.query.\
        filter_by(tournament_id=tournament_id, name=cat.name).first()

    if dao is None:
        score_args = {
            'tournament_id': tournament_id,
            'name':          cat.name,
            'percentage':    cat.percentage,
            'per_tourn':     cat.per_tournament,
            'min_val':       cat.min_val,
            'max_val':       cat.max_val
        }

        dao = ScoreCategory(**score_args)
    dao.set_percentage(cat.percentage)
    dao.per_tournament = cat.per_tournament
    db.session.add(dao)
    db.session.flush()


def validate_score(score, category, game_id=None):
    """Validate an entered score. Returns True or raises Exception"""
    try:
        score = int(score)
        if score < category.min_val or score > category.max_val:
            raise ValueError()

        if game_id and category.per_tournament:
            raise TypeError('Cannot enter a per-tournament score '\
                '({}) for a game (game_id: {})'.\
                format(category.name, game_id))

        if game_id is None and not category.per_tournament:
            raise TypeError('{} should be entered per-tournament'.\
                format(category.name))
    except ValueError:
        raise ValueError('Invalid score: {}'.format(score))


def write_score(tournament, entry_id, score_cat, score, game_id=None):
    """
    Enters a score for category into tournament for player.

    Expects: All fields required
        - entry_id - of the entry
        - score_cat - e.g. round_3_battle
        - score - integer

    Returns: Nothing on success. Throws ValueErrors and RuntimeErrors when
        there is an issue inserting the score.
    """
    # score_cat should mean something in the context of the tournie
    cat = db.session.query(ScoreCategory).filter_by(
        tournament_id=tournament.name, name=score_cat).first()

    try:
        validate_score(score, cat, game_id)
    except AttributeError:
        raise TypeError('Unknown category: {}'.format(score_cat))

    # Has it already been entered?
    if game_id is None:
        # pylint: disable=no-member
        existing_score = TournamentScore.query.join(Score).\
            join(ScoreCategory).\
            filter(and_(
                TournamentScore.entry_id == entry_id,
                TournamentScore.tournament_id == tournament.id,
                ScoreCategory.id == cat.id)).first() is not None
    else:
        try:
            # pylint: disable=no-member
            existing_score = GameScore.query.join(Score).\
                filter(and_(GameScore.entry_id == entry_id, \
                            GameScore.game_id == game_id,
                            Score.score_category_id == cat.id)).\
                first() is not None
        except DataError:
            db.session.rollback()
            raise AttributeError('{} not entered. Game {} cannot be found'.\
                format(score, game_id))

    if existing_score:
        raise ValueError(
            '{} not entered. Score is already set'.format(score))

    try:
        score_dao = Score(entry_id, cat.id, score)
        db.session.add(score_dao)
        db.session.flush()

        if game_id is not None:
            db.session.add(GameScore(entry_id, game_id, score_dao.id))
        else:
            db.session.add(
                TournamentScore(entry_id, tournament.id, score_dao.id))
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        if 'is not present in table "entry"' in err.__repr__():
            raise AttributeError('{} not entered. Entry {} doesn\'t exist'.\
                format(score, entry_id))
        elif 'is not present in table "game"' in err.__repr__():
            raise AttributeError('{} not entered. Game {} cannot be found'.\
                format(score, game_id))
        raise err


# pylint: disable=too-many-arguments
class ScoreCategoryPair(object):
    """A holder object for score category information"""
    def __init__(self, name, percentage, per_tourn, min_val, max_val):
        if not name:
            raise ValueError('Category must have a name')

        self.percentage = percentage

        try:
            self.min_val = int(min_val)
            self.max_val = int(max_val)
        except ValueError:
            raise ValueError('Min and Max Scores must be integers')
        except TypeError:
            raise ValueError('Min and Max Scores must be integers')

        self.name = name
        self.per_tournament = per_tourn
