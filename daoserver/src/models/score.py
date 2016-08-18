"""
Logic for scores goes here
"""
from models.dao.db_connection import db

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
        dao = ScoreCategory(tournament_id,
                            cat.name,
                            cat.percentage,
                            cat.per_tournament,
                            cat.min_val,
                            cat.max_val,)
    dao.percentage = int(cat.percentage)
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


# pylint: disable=too-many-arguments
class ScoreCategoryPair(object):
    """A holder object for score category information"""
    def __init__(self, name, percentage, per_tourn, min_val, max_val):
        if not name:
            raise ValueError('Category must have a name')

        try:
            self.percentage = int(percentage)
            if self.percentage > 100 or self.percentage < 1:
                raise ValueError()
        except ValueError:
            raise ValueError('Percentage must be an integer (1-100)')

        try:
            self.min_val = int(min_val)
            self.max_val = int(max_val)
        except ValueError:
            raise ValueError('Min and Max Scores must be integers')
        except TypeError:
            raise ValueError('Min and Max Scores must be integers')

        self.name = name
        self.per_tournament = per_tourn
