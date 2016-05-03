"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import and_

from matching_strategy import RoundRobin
from models.score import db as score_db, Score, RoundScore, ScoreCategory, \
ScoreKey, scores_for_entry
from models.table_allocation import TableAllocation
from models.tournament import Tournament as TournamentDB
from models.tournament_entry import TournamentEntry
from models.tournament_game import TournamentGame as Game
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
            entry.scores = scores_for_entry(entry.id)

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
    def make_draw(self, round_id=0):
        """Determines the draw for round. This draw is written to the db"""
        match_ups = self.matching_strategy.match(int(round_id), self.entries())
        draw = self.table_strategy.determine_tables(match_ups)
        try:
            for match in draw:

                game = Game(tournament=self.tournament_id,
                            round_num=round_id,
                            table_num=match.table_number)
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

        return draw

    @must_exist_in_db
    def get_round(self, round_num):
        """Get the relevant TournamentRound"""
        try:
            return [x for x in self.rounds if x.round_num == int(round_num)][0]
        except IndexError:
            raise ValueError('Tournament {} does not have a round {}'.format(
                self.tournament_id, round_num))

    @must_exist_in_db
    def round_info(self, round_id=0):
        """
        Returns info about round.
        Returns:
            - dict with three keys {score_keys, draw, mission}
        """
        draw = [
            {'table_number':t.table_number,
             'entrants': [x if isinstance(x, str) else x.player_id \
                          for x in t.entrants]
            } for t in self.make_draw(round_id)]

        return {
            'score_keys': self.get_score_keys_for_round(round_id),
            'draw': draw,
            'mission': self.get_round(round_id).get_mission()
        }

    @must_exist_in_db
    def set_number_of_rounds(self, num_rounds):
        """Set the number of rounds in a tournament"""
        tourn = self.get_dao()
        tourn.num_rounds = int(num_rounds)
        tourn.write()

        for rnd in [x for x in self.rounds if x.round_num > tourn.num_rounds]:
            if rnd.get_dao() is not None:
                rnd.get_dao().delete()

        self.rounds = [TournamentRound(self.tournament_id, x) \
            for x in range(1, num_rounds + 1)]

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

    @must_exist_in_db
    def get_score_keys_for_round(self, round_id='next'):
        """
        Get all the score keys associated with this round
        Returns a list of tuples:
            (id, key, min, max, category_id, score_key_id, round_id)
        """

        #TODO get next round
        if round_id == 'next':
            raise NotImplementedError('next round is unknown')

        results = score_db.session.query(ScoreKey, RoundScore).\
            join(RoundScore).filter_by(round_id=round_id).all()

        if len(results) == 0:
            raise ValueError("Draw not ready. Mission not set. Contact TO")

        return [
            (x[0].id, x[0].key, x[0].min_val, x[0].max_val, x[0].category,
             x[1].score_key_id, x[1].round_id) for x in results]

class ScoreCategoryPair(object):
    """A holder object for score category information"""
    def __init__(self, name, percentage, per_tourn):
        self.name = name
        self.percentage = float(percentage)
        if self.percentage <= 0 or self.percentage > 100:
            raise ValueError("Score categories must be between 1 and 100")
        self.per_tournament = per_tourn
