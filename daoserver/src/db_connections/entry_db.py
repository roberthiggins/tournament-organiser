"""
This file contains code to connect to the entry_db
"""

from flask import json
import psycopg2
from psycopg2.extras import DictCursor
from sqlalchemy.sql.expression import and_

from db_connections.db_connection import db_conn
from models.db_connection import db
from models.score import ScoreCategory, ScoreKey
from models.tournament_entry import TournamentEntry

class Entry(json.JSONEncoder):
    """
    A tournament is composed of entries who play each other. This is distinct
    from users or accounts as there may be multiple players on a team, etc.
    """

    #pylint: disable=R0913
    def __init__(
            self,
            entry_id=None,
            username=None,
            tournament_id=None,
            game_history=None,
            scores=None):
        self.entry_id = entry_id
        self.username = username
        self.tournament_id = tournament_id
        self.game_history = game_history
        self.ranking = None
        self.scores = scores
        self.total_score = 0

    def __repr__(self):
        return self.entry_id

# pylint: disable=no-member
class EntryDBConnection(object):
    """
    Connection class to the entry database
    """

    @db_conn(commit=True)
    # pylint: disable=E0602
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
        try:
            tournament_name = TournamentEntry.query.\
                filter_by(id=entry_id).first().tournament.name

            # score_key should mean something in the context of the tournie
            key = db.session.query(ScoreKey).join(ScoreCategory).\
                filter(and_(ScoreCategory.tournament_id == tournament_name,
                            ScoreKey.key == score_key)
                      ).first()

            score = int(score)
            if score < key.min_val or score > key.max_val:
                raise ValueError()

            cur.execute(
                "INSERT INTO score VALUES(%s, %s, %s)",
                [entry_id, key.id, score])

        except AttributeError:
            raise TypeError('Unknown category: {}'.format(score_key))
        except TypeError:
            raise TypeError('Unknown category: {}'.format(score_key))
        except ValueError:
            raise ValueError('Invalid score: %s' % score)
        except psycopg2.DataError:
            raise ValueError('Invalid score: %s' % score)
        except psycopg2.IntegrityError:
            raise ValueError(
                '{} not entered. Score is already set'.format(score))

    @db_conn(cursor_factory=DictCursor)
    # pylint: disable=E0602
    def entry_list(self, tournament_id):
        """
        Get the list of entries for the specified tournament.
        This simply returns a dump of entries and their info in a big list.
        """
        cur.execute(
            "SELECT \
                e.id                                    AS entry_id, \
                a.username                              AS username, \
                t.name                                  AS tournament_id, \
                (SELECT array(SELECT table_no \
                    FROM table_allocation \
                    WHERE entry_id = e.id))             AS game_history \
            FROM entry e \
            INNER JOIN account a on e.player_id = a.username \
            INNER JOIN tournament t on e.tournament_id = t.name \
            WHERE t.name = %s",
            [tournament_id])
        entries = cur.fetchall()

        unranked_list = [
            Entry(
                entry_id=entry['entry_id'],
                username=entry['username'],
                tournament_id=entry['tournament_id'],
                game_history=entry['game_history'],
                scores=self.get_scores_for_entry(entry['entry_id']),
            ) for entry in entries
        ]

        return unranked_list

    @db_conn()
    # pylint: disable=E0602
    def get_scores_for_entry(self, entry_id):
        """ Get all the score_key:score pairs for an entry"""
        cur.execute("SELECT key, score, category, min_val, max_val \
            FROM player_score WHERE entry_id = %s", [entry_id])
        return [
            {
                'key': x[0],
                'score':x[1],
                'category': x[2],
                'min_val': x[3],
                'max_val': x[4],
            } for x in cur.fetchall()
        ]
