"""
Model of a tournament

It holds a tournament object for housing of scoring strategies, etc.
"""
import datetime

from sqlalchemy.sql.expression import and_

from db_connections.entry_db import EntryDBConnection
from matching_strategy import RoundRobin
from models.score import db as score_db, RoundScore, ScoreCategory, ScoreKey
from models.tournament import Tournament as TournamentDB
from models.tournament_round import TournamentRound
from permissions import PermissionsChecker, PERMISSIONS
from ranking_strategies import RankingStrategy
from table_strategy import ProtestAvoidanceStrategy

def must_exist_in_db(func):
    """ A decorator that requires the tournament exists in the db"""
    def wrapped(self, *args, **kwargs):                 # pylint: disable=C0111
        if not self.exists_in_db:
            print 'Tournament not found: {}'.format(self.tournament_id)
            raise ValueError(
                'Tournament {} not found in database'.format(
                    self.tournament_id))
        return func(self, *args, **kwargs)
    return wrapped

# pylint: disable=E1101
class Tournament(object):
    """A tournament DAO"""

    def __init__(self, tournament_id=None, ranking_strategy=None, creator=None):
        self.tournament_id = tournament_id
        self.exists_in_db = TournamentDB.query.filter_by(
            name=tournament_id).first() is not None
        self.ranking_strategy = \
            ranking_strategy(tournament_id, self.list_score_categories) \
            if ranking_strategy \
            else RankingStrategy(tournament_id, self.list_score_categories)
        self.matching_strategy = RoundRobin(tournament_id)
        self.table_strategy = ProtestAvoidanceStrategy()
        self.creator_username = creator

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

    @must_exist_in_db
    def create_score_category(self, category, percentage):
        """ Add a score category """
        ScoreCategory(self.tournament_id, category, percentage).write()

    @must_exist_in_db
    def details(self):
        """
        Get details about a tournament. This includes entrants and format
        information
        """
        details = TournamentDB.query.filter_by(name=self.tournament_id).first()

        return {
            'name': details.name,
            'date': details.date,
            'rounds': details.num_rounds,
        }

    @must_exist_in_db
    def list_score_categories(self):
        """
        List all the score categories available to this tournie and their
        percentages.
        [{ 'name': 'Painting', 'percentage': 20, 'id': 1 }]
        """
        categories = ScoreCategory.query.\
            filter_by(tournament_id=self.tournament_id).all()
        return [
            {'id': x.id, 'name': x.display_name, 'percentage': x.percentage} \
            for x in categories]

    @must_exist_in_db
    def make_draw(self, round_id=0):
        """Determines the draw for round. This draw is written to the db"""
        match_ups = self.matching_strategy.match(int(round_id))
        draw = self.table_strategy.determine_tables(match_ups)
        try:
            from game import Game
            for match in draw:
                game = Game(match.entrants,
                            tournament_id=self.tournament_id,
                            round_id=round_id,
                            table_number=match.table_number)
                game.write_to_db()
                if game.entry_1 is not None:
                    entry_id = game.entry_1
                    uname = EntryDBConnection().entry_info(entry_id)['username']
                    PermissionsChecker().add_permission(
                        uname,
                        PERMISSIONS['ENTER_SCORE'],
                        game.protected_object_id)
                if game.entry_2 is not None:
                    entry_id = game.entry_2
                    uname = EntryDBConnection().entry_info(entry_id)['username']
                    PermissionsChecker().add_permission(
                        uname,
                        PERMISSIONS['ENTER_SCORE'],
                        game.protected_object_id)

                # The person playing the bye gets no points at the time
                if None in [game.entry_1, game.entry_2]:
                    game.set_score_entered()

        except ValueError as err:
            if 'duplicate key value violates unique constraint "game_pkey"' \
            not in str(err):
                raise err

        return draw

    @must_exist_in_db
    def get_mission(self, round_id):
        """Get the mission for a given round"""

        tournament_round = TournamentRound.query.\
            filter(and_(TournamentRound.tournament_name == self.tournament_id,
                        TournamentRound.ordering == int(round_id))
                  ).first()

        if tournament_round is not None:
            return tournament_round.mission
        raise ValueError('Round {} does not exist'.format(round_id))

    @must_exist_in_db
    def get_missions(self):
        """Get all missions for the tournament"""
        rounds = TournamentRound.query.\
            filter_by(tournament_name=self.tournament_id).all()
        return [x.mission for x in rounds]

    @must_exist_in_db
    def round_info(self, round_id=0):
        """
        Returns info about round.
        Returns:
            - dict with three keys {score_keys, draw, mission}
        """
        return {
            'score_keys': self.get_score_keys_for_round(round_id),
            'draw': self.make_draw(round_id),
            'mission': self.get_mission(round_id)
        }

    @must_exist_in_db
    def set_mission(self, round_id, mission):
        """Set the mission for a given round"""
        round_id = int(round_id)
        tournament_round = TournamentRound.query.\
            filter_by(tournament_name=self.tournament_id, ordering=round_id).\
            first()

        if tournament_round is None:
            TournamentRound(self.tournament_id, round_id, mission).write()
        else:
            tournament_round.mission = mission
            tournament_round.write()

    @must_exist_in_db
    def set_number_of_rounds(self, num_rounds):
        """Set the number of rounds in a tournament"""
        tourn = TournamentDB.query.filter_by(name=self.tournament_id).first()
        tourn.num_rounds = int(num_rounds)
        tourn.write()

        rounds = TournamentRound.query.filter(
            and_(
                TournamentRound.tournament_name == self.tournament_id,
                TournamentRound.ordering > int(num_rounds))
            ).all()

        for extra_round in rounds:
            extra_round.delete()

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
        """ Get all the score keys associated with this round"""

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
