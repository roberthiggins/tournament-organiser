"""
Logic for scores goes here
"""

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

