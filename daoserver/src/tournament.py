"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import and_

from matching_strategy import RoundRobin
from models.score import db as score_db, Score, RoundScore, ScoreCategory, \
ScoreKey
from models.table_allocation import TableAllocation
from models.tournament import Tournament as TournamentDB
from models.tournament_entry import TournamentEntry
from models.tournament_game import TournamentGame
from permissions import PermissionsChecker, PERMISSIONS
from ranking_strategies import RankingStrategy
from table_strategy import ProtestAvoidanceStrategy
from tournament_round import TournamentRound

def must_exist_in_db(func):
    """ A decorator that requires the tournament exists in the db"""
    def wrapped(self, *args, **kwargs):                 # pylint: disable=missing-docstring
        if not self.exists_in_db:
            print 'Tournament not found: {}'.format(self.tournament_id)
            raise ValueError(
                'Tournament {} not found in database'.format(
                    self.tournament_id))
        return func(self, *args, **kwargs)
    return wrapped

# pylint: disable=no-member
class Tournament(object):
    """A tournament DAO"""

    def __init__(self, tournament_id=None, ranking_strategy=None, creator=None):
        self.tournament_id = tournament_id
        self.exists_in_db = self.get_dao() is not None
        self.ranking_strategy = \
            ranking_strategy(tournament_id, self.list_score_categories) \
            if ranking_strategy \
            else RankingStrategy(tournament_id, self.list_score_categories)
        self.matching_strategy = RoundRobin()
        self.table_strategy = ProtestAvoidanceStrategy()
        self.creator_username = creator
        if self.exists_in_db:
            self.rounds = [TournamentRound(self.tournament_id, rnd) \
                for rnd in range(1, self.get_dao().num_rounds + 1)]
        else:
            self.rounds = []

    def add_to_db(self, date):
        """
        add a tournament
        Expects:
            - inputTournamentDate - Tournament Date. YYYY-MM-DD
        """
        if self.exists_in_db:
            raise RuntimeError('A tournament with name {} already exists! \
            Please choose another name'.format(self.tournament_id))

        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        if date.date() < datetime.date.today():
            raise ValueError('Enter a valid date')

        dao = TournamentDB(self.tournament_id)
        dao.date = date
        dao.write()

        PermissionsChecker().add_permission(
            self.creator_username,
            PERMISSIONS['ENTER_SCORE'],
            dao.protected_object_id)

    def get_dao(self):
        """Convenience method to recover DAO"""
        return TournamentDB.query.filter_by(name=self.tournament_id).first()

    @must_exist_in_db
    def set_score_categories(self, new_categories):
        """
        Replace the existing score categories with those from the list. The list
        should contain a ScoreCategorys
        """

        # check for duplicates
        keys = [x.name for x in new_categories]
        if len(keys) != len(set(keys)):
            raise ValueError("You cannot set multiple keys with the same name")

        to_delete = ScoreCategory.query.\
            filter_by(tournament_id=self.tournament_id).all()

        for cat in new_categories:
            dao = ScoreCategory.query.\
                filter_by(tournament_id=self.tournament_id,
                          display_name=cat.name).first()

            if dao is None:
                dao = ScoreCategory(self.tournament_id,
                                    cat.name,
                                    cat.percentage,
                                    cat.per_tournament)
            else:
                to_delete = [x for x in to_delete if x.display_name != cat.name]
            dao.percentage = int(cat.percentage)
            dao.per_tournament = cat.per_tournament
            dao.write()

        for cat in to_delete:
            cat.delete()

    @must_exist_in_db
    def details(self):
        """
        Get details about a tournament. This includes entrants and format
        information
        """
        details = self.get_dao()

        return {
            'name': details.name,
            'date': details.date,
            'rounds': details.num_rounds,
        }

    @must_exist_in_db
    def enter_score(self, entry_id, score_key, score):
        """
        Enters a score for category into tournament for player.

        Expects: All fields required
            - entry_id - of the entry
            - score_key - e.g. round_3_battle
            - score - integer

        Returns: Nothing on success. Throws ValueErrors and RuntimeErrors when
            there is an issue inserting the score.
        """
        # score_key should mean something in the context of the tournie
        key = score_db.session.query(ScoreKey).join(ScoreCategory).\
            filter(and_(ScoreCategory.tournament_id == self.get_dao().name,
                        ScoreKey.key == score_key)
                  ).first()

        try:
            score = int(score)
            if score < key.min_val or score > key.max_val:
                raise ValueError()
        except ValueError:
            raise ValueError('Invalid score: {}'.format(score))
        except AttributeError:
            raise TypeError('Unknown category: {}'.format(score_key))

        try:
            Score(entry_id, key.id, score).write()
        except IntegrityError:
            raise ValueError(
                '{} not entered. Score is already set'.format(score))

    @must_exist_in_db
    def entries(self):
        """Get a list of Entry"""

        entries = TournamentEntry.query.\
            filter_by(tournament_id=self.tournament_id).all()
        for entry in entries:
            entry.game_history = [x.table_no for x in \
                TableAllocation.query.filter_by(entry_id=entry.id)]
            entry.score_info = [
                {
                    'key': x.score_key.key,
                    'score': x.value,
                    'category': x.score_key.score_category.display_name,
                    'min_val': x.score_key.min_val,
                    'max_val': x.score_key.max_val,
                } for x in entry.scores
            ]

        return entries

    @must_exist_in_db
    def list_score_categories(self):
        """
        List all the score categories available to this tournie and their
        percentages.
        [{ 'name': 'Painting', 'percentage': 20, 'id': 1,
           'per_tournament': False }]
        """
        categories = ScoreCategory.query.\
            filter_by(tournament_id=self.tournament_id).all()
        return [
            {'id': x.id,
             'name': x.display_name,
             'percentage': x.percentage,
             'per_tournament': x.per_tournament} for x in categories]

    @must_exist_in_db
    def make_draw(self, round_id=1):
        """Determines the draw for round. This draw is written to the db"""
        rnd = self.get_round(round_id)
        match_ups = self.matching_strategy.match(rnd.round_num, self.entries())
        rnd.draw = self.table_strategy.determine_tables(match_ups)
        try:
            for match in rnd.draw:

                game = TournamentGame(rnd.get_dao().id, match.table_number)
                entrants = [None if x == 'BYE' else x for x in match.entrants]

                for entrant in entrants:
                    if entrant is not None:
                        uname = TournamentEntry.query.\
                            filter_by(id=entrant.id).first().player_id
                        PermissionsChecker().add_permission(
                            uname,
                            PERMISSIONS['ENTER_SCORE'],
                            game.protected_object.id)
                    else:
                        # The person playing the bye gets no points at the time
                        game.score_entered = True

                game.write()

        except IntegrityError as err:
            if 'duplicate key' not in str(err):
                raise err

    @must_exist_in_db
    def get_round(self, round_num):
        """Get the relevant TournamentRound"""
        try:
            return [x for x in self.rounds if x.round_num == int(round_num)][0]
        except IndexError:
            raise ValueError('Tournament {} does not have a round {}'.format(
                self.tournament_id, round_num))

    @must_exist_in_db
    def set_number_of_rounds(self, num_rounds):
        """Set the number of rounds in a tournament"""
        tourn = self.get_dao()
        tourn.num_rounds = int(num_rounds)
        tourn.write()

        from models.tournament_round import TournamentRound as TR
        for rnd in tourn.rounds.filter(TR.ordering > tourn.num_rounds).all():
            rnd.round_scores.delete()
            rnd.games.delete()
        tourn.rounds.filter(TR.ordering > tourn.num_rounds).delete()
        from models.db_connection import db
        db.session.commit()

        self.rounds = [TournamentRound(self.tournament_id, x) \
            for x in range(1, tourn.num_rounds + 1)]

    @must_exist_in_db
    # pylint: disable=R0913
    def set_score(self, key, category, min_val=0, max_val=20, round_id=None):
        """
        Set a score category that a player is eligible for in a tournament.

        For example, use this to specify that a tourn has a 'round_1_battle'
        score for each player.

        Expected:
            - key - unique name e.g. round_4_comp
            - (opt) min_val - for score - default 0
            - (opt) max_val - for score - default 20
            - (opt) round_id - the score is for the round
        """
        if not min_val:
            min_val = 0
        if not max_val:
            max_val = 20

        key = ScoreKey(key, category, min_val, max_val)
        key.write()

        # This score could be per-game rather than per-tournament
        if round_id is not None:
            RoundScore(key.id, round_id).write()

class ScoreCategoryPair(object):
    """A holder object for score category information"""
    def __init__(self, name, percentage, per_tourn):
        self.name = name
        self.percentage = float(percentage)
        if self.percentage <= 0 or self.percentage > 100:
            raise ValueError("Score categories must be between 1 and 100")
        self.per_tournament = per_tourn
