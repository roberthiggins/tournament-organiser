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

