"""
Logic for scores goes here
"""
from sqlalchemy.exc import IntegrityError
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
            format(game_dao.tournament_round.tournament.name))

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
        filter_by(tournament_id=tournament_id, name=cat['name']).first()

    cat['tournament_id'] = tournament_id

    if dao is None:
        dao = ScoreCategory(**cat)
    else:
        dao.update(**cat)

    db.session.add(dao)
    db.session.flush()


def validate_score(score, category, entry, game=None):
    """Validate an entered score. Returns True or raises Exception"""
    invalid_score = ValueError('Invalid score: {}'.format(score))
    score = int(score)
    if score < category.min_val or score > category.max_val:
        raise invalid_score

    if game is None and not category.per_tournament:
        raise TypeError('{} should be entered per-tournament'.\
            format(category.name))

    if game is not None and category.per_tournament:
        raise TypeError('Cannot enter a per-tournament score '\
            '({}) for a game (id: {})'.\
            format(category.name, game.id))

    # If zero sum we need to check the score entered by the opponent
    if game is not None and category.zero_sum:
        # pylint: disable=no-member
        game_scores = GameScore.query.join(Score, ScoreCategory).\
                filter(and_(GameScore.game_id == game.id,
                            ScoreCategory.name == category.name,
                            GameScore.entry_id != entry.id)).all()
        existing_score = sum([x.score.value for x in game_scores])
        if existing_score + score > category.max_val:
            raise invalid_score


def write_score(tournament, entry, category, score, game=None):
    """
    Enters a score for category into tournament for player.

    Expects: All fields required
        - score - integer

    Returns: Nothing on success. Throws ValueErrors and RuntimeErrors when
        there is an issue inserting the score.
    """
    # pylint: disable=no-member
    # Has it already been entered?
    if game is None:
        existing_score = TournamentScore.query.join(Score).\
            join(ScoreCategory).\
            filter(and_(
                TournamentScore.entry_id == entry.id,
                TournamentScore.tournament_id == tournament.id,
                ScoreCategory.id == category.id)).first()
    else:
        existing_score = GameScore.query.join(Score).\
            filter(and_(GameScore.entry_id == entry.id, \
                        GameScore.game_id == game.id,
                        Score.score_category_id == category.id)).first()

    if existing_score is not None:
        raise ValueError(
            '{} not entered. Score is already set'.format(score))

    try:
        score_dao = Score(entry.id, category.id, score)
        db.session.add(score_dao)
        db.session.flush()

        if game is not None:
            db.session.add(GameScore(entry.id, game.id, score_dao.id))
        else:
            db.session.add(
                TournamentScore(entry.id, tournament.id, score_dao.id))
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        if 'is not present in table "entry"' in err.__repr__():
            raise AttributeError('{} not entered. Entry {} doesn\'t exist'.\
                format(score, entry.id))
        raise err
