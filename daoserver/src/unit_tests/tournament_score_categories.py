"""
Test entering scores for games in a tournament
"""

from flask_testing import TestCase
from testfixtures import compare

from app import create_app
from models.dao.db_connection import db
from models.dao.score import ScoreCategory

from models.tournament import Tournament
from unit_tests.tournament_injector import score_cat_args as cat, \
TournamentInjector

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
        self.injector.inject(self.tourn_1)
        db.session.flush()
        db.session.commit()

        # Some default categories
        self.cat_1 = cat(self.tourn_1, 'painting', 10, False, 1, 20)
        self.cat_2 = cat(self.tourn_1, 'cat_battle', 80, True, 1, 20)
        self.cat_3 = cat(self.tourn_1, 'cat_sports', 10, True, 1, 5)

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
        compare(c_1.per_tournament, self.cat_1['per_tournament'])
        compare(c_1.min_val, self.cat_1['min_val'])
        compare(c_1.max_val, self.cat_1['max_val'])

        # Enter multiple cats
        self.tournament.set_score_categories([self.cat_2, self.cat_3])
        c_2 = ScoreCategory.query.\
            filter_by(name=self.cat_2['name']).first()
        compare(c_2.percentage, self.cat_2['percentage'])
        compare(c_2.per_tournament, self.cat_2['per_tournament'])
        compare(c_2.min_val, self.cat_2['min_val'])
        compare(c_2.max_val, self.cat_2['max_val'])

        c_3 = ScoreCategory.query.\
            filter_by(name=self.cat_3['name']).first()
        compare(c_3.percentage, self.cat_3['percentage'])
        compare(c_3.per_tournament, self.cat_3['per_tournament'])
        compare(c_3.min_val, self.cat_3['min_val'])
        compare(c_3.max_val, self.cat_3['max_val'])

    def test_old_categories_deleted(self):
        self.tournament.set_score_categories([self.cat_1])
        self.tournament.set_score_categories([self.cat_2, self.cat_3])

        # Double check cat 1 is deleted.
        compare(0, ScoreCategory.query.filter_by(name=self.cat_1['name']).\
            count())


    # pylint: disable=unused-variable
    def test_broken_min_max(self):
        neg_min = cat(self.tourn_1, 'painting', 10, False, -1, 20)
        neg_max = cat(self.tourn_1, 'painting', 10, False, 1, -1)
        zero_max = cat(self.tourn_1, 'painting', 10, False, 0, 0)
        min_high = cat(self.tourn_1, 'painting', 10, False, 10, 9)
        zero_min = cat(self.tourn_1, 'painting', 10, False, 0, 20)
        equal = cat(self.tourn_1, 'painting', 10, False, 1, 1)
        no_min = cat(self.tourn_1, 'painting', '10', False, '', 20)
        no_max = cat(self.tourn_1, 'painting', '10', False, 1, '')
        none_min = cat(self.tourn_1, 'painting', '1', False, None, 1)
        none_max = cat(self.tourn_1, 'painting', '1', False, 1, None)
        char_min = cat(self.tourn_1, 'painting', '1', False, 'a', 1)
        char_max = cat(self.tourn_1, 'painting', '1', False, 1, 'a')

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
        # cat should perform input validation only
        fifty_one = cat(self.tourn_1, 'painting', 51, False, 1, 20)
        neg_pct = cat(self.tourn_1, 'painting', -1, False, 1, 20)
        zero_pct = cat(self.tourn_1, 'painting', 0, False, 1, 20)
        lge_pct = cat(self.tourn_1, 'painting', 101, False, 1, 20)
        char_pct = cat(self.tourn_1, 'painting', 'a', False, 1, 20)
        no_name = cat(self.tourn_1, '', 10, False, 1, 20)
        none_name = cat(self.tourn_1, None, 10, False, 1, 20)

        set_cats_func = self.tournament.set_score_categories
        self.assertRaises(ValueError, set_cats_func, [neg_pct])
        self.assertRaises(ValueError, set_cats_func, [zero_pct])
        self.assertRaises(ValueError, set_cats_func, [lge_pct])
        self.assertRaises(ValueError, set_cats_func, [char_pct])
        self.assertRaises(ValueError, set_cats_func, [no_name])
        self.assertRaises(ValueError, set_cats_func, [none_name])
        self.assertRaises(ValueError, set_cats_func, [fifty_one, fifty_one])
