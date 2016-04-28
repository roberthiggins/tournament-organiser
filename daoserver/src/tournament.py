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
from models.tournament import Tournament as TournamentDB
from models.tournament_entry import TournamentEntry
from models.tournament_game import TournamentGame as Game
from models.tournament_round import TournamentRound
from permissions import PermissionsChecker, PERMISSIONS
from ranking_strategies import RankingStrategy
from table_strategy import ProtestAvoidanceStrategy

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
    def create_score_category(self, category, percentage):
        """ Add a score category """
        ScoreCategory(self.tournament_id, category, percentage).write()

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

        def scores_for_entry(entry_id):
            """ Get all the score_key:score pairs for an entry"""

            scores = score_db.session.query(Score, ScoreKey, ScoreCategory).\
                join(ScoreKey).join(ScoreCategory).join(TournamentDB).\
                join(TournamentEntry).filter(Score.entry_id == entry_id).\
                all()

            return [
                {
                    'key': x[1].key,
                    'score':x[0].value,
                    'category': x[2].display_name,
                    'min_val': x[1].min_val,
                    'max_val': x[1].max_val,
                } for x in scores
            ]

        from models.table_allocation import TableAllocation
        from entry import Entry
        entries = TournamentEntry.query.\
            filter_by(tournament_id=self.tournament_id).all()

        return [
            Entry(
                entry_id=entry.id,
                username=entry.account.username,
                tournament_id=entry.tournament.name,
                game_history=[x.table_no for x in \
                    TableAllocation.query.filter_by(entry_id=entry.id)],
                scores=scores_for_entry(entry.id),
            ) for entry in entries
        ]

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
                            filter_by(id=entrant.entry_id).first().player_id
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
        tourn = self.get_dao()
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
