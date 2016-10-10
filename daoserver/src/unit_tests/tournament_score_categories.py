"""
Test entering scores for games in a tournament
"""

from flask_testing import TestCase
from testfixtures import compare

from app import create_app
from models.dao.db_connection import db
from models.dao.score import ScoreCategory

from models.tournament import Tournament
from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=too-many-arguments
def score_cat_args(name, pct, per_tourn, min_val, max_val, zero_sum=False):
    """Convenience function to make a ScoreCategory args blob"""
    return {
        'name':       name,
        'percentage': pct,
        'per_tourn':  per_tourn,
        'min_val':    min_val,
        'max_val':    max_val,
        'zero_sum':   zero_sum}

# pylint: disable=no-member,invalid-name,missing-docstring
class ScoreCategoryTests(TestCase):
    """Comes from a range of files"""

    tourn_1 = 'test_score_categories'

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()

        # Some default categories
        self.cat_1 = score_cat_args('categories_painting', 10, False, 1, 20)
        self.cat_2 = score_cat_args('categories_battle', 80, True, 1, 20)
        self.cat_3 = score_cat_args('categories_sports', 10, True, 1, 5)

        # We will make a tournament with 5 entrants.
        self.injector.inject(self.tourn_1)
        self.tournament = Tournament(self.tourn_1)

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

    def test_categories_created(self):
        # Enter a cat
        self.tournament.set_score_categories([self.cat_1])
        c_1 = ScoreCategory.query.\
            filter_by(name=self.cat_1['name']).first()
        compare(c_1.percentage, self.cat_1['percentage'])
        compare(c_1.per_tournament, self.cat_1['per_tourn'])
        compare(c_1.min_val, self.cat_1['min_val'])
        compare(c_1.max_val, self.cat_1['max_val'])

        # Enter multiple cats
        self.tournament.set_score_categories([self.cat_2, self.cat_3])
        c_2 = ScoreCategory.query.\
            filter_by(name=self.cat_2['name']).first()
        compare(c_2.percentage, self.cat_2['percentage'])
        compare(c_2.per_tournament, self.cat_2['per_tourn'])
        compare(c_2.min_val, self.cat_2['min_val'])
        compare(c_2.max_val, self.cat_2['max_val'])

        c_3 = ScoreCategory.query.\
            filter_by(name=self.cat_3['name']).first()
        compare(c_3.percentage, self.cat_3['percentage'])
        compare(c_3.per_tournament, self.cat_3['per_tourn'])
        compare(c_3.min_val, self.cat_3['min_val'])
        compare(c_3.max_val, self.cat_3['max_val'])

    def test_old_categories_deleted(self):
        self.tournament.set_score_categories([self.cat_1])
        self.tournament.set_score_categories([self.cat_2, self.cat_3])

        # Double check cat 1 is deleted.
        c_1 = ScoreCategory.query.\
            filter_by(name=self.cat_1['name']).first()
        self.assertTrue(c_1 is None)


    # pylint: disable=unused-variable
    def test_broken_min_max(self):
        neg_min = score_cat_args('categories_painting', 10, False, -1, 20)
        neg_max = score_cat_args('categories_painting', 10, False, 1, -1)
        zero_max = score_cat_args('categories_painting', 10, False, 0, 0)
        min_high = score_cat_args('categories_painting', 10, False, 10, 9)
        zero_min = score_cat_args('categories_painting', 10, False, 0, 20)
        equal = score_cat_args('categories_painting', 10, False, 1, 1)
        no_min = score_cat_args('categories_painting', '10', False, '', 20)
        no_max = score_cat_args('categories_painting', '10', False, 1, '')
        none_min = score_cat_args('categories_painting', '1', False, None, 1)
        none_max = score_cat_args('categories_painting', '1', False, 1, None)
        char_min = score_cat_args('categories_painting', '1', False, 'a', 1)
        char_max = score_cat_args('categories_painting', '1', False, 1, 'a')

        set_cats_func = self.tournament.set_score_categories
        self.assertRaises(ValueError, set_cats_func, [neg_min])
        self.assertRaises(ValueError, set_cats_func, [neg_max])
        self.assertRaises(ValueError, set_cats_func, [zero_max])
        self.assertRaises(ValueError, set_cats_func, [min_high])
        self.assertRaises(ValueError, set_cats_func, [no_min])
        self.assertRaises(ValueError, set_cats_func, [no_max])
        self.assertRaises(ValueError, set_cats_func, [none_min])
        self.assertRaises(ValueError, set_cats_func, [none_max])
        self.assertRaises(ValueError, set_cats_func, [char_min])
        self.assertRaises(ValueError, set_cats_func, [char_max])


    def test_broken_categories(self):
        # score_cat_args should perform input validation only
        fifty_one = score_cat_args('categories_painting', 51, False, 1, 20)
        neg_pct = score_cat_args('categories_painting', -1, False, 1, 20)
        zero_pct = score_cat_args('categories_painting', 0, False, 1, 20)
        lge_pct = score_cat_args('categories_painting', 101, False, 1, 20)
        char_pct = score_cat_args('categories_painting', 'a', False, 1, 20)
        no_name = score_cat_args('', 10, False, 1, 20)
        none_name = score_cat_args(None, 10, False, 1, 20)

        set_cats_func = self.tournament.set_score_categories
        self.assertRaises(ValueError, set_cats_func, [neg_pct])
        self.assertRaises(ValueError, set_cats_func, [zero_pct])
        self.assertRaises(ValueError, set_cats_func, [lge_pct])
        self.assertRaises(ValueError, set_cats_func, [char_pct])
        self.assertRaises(ValueError, set_cats_func, [no_name])
        self.assertRaises(ValueError, set_cats_func, [none_name])
        self.assertRaises(ValueError, set_cats_func, [fifty_one, fifty_one])
