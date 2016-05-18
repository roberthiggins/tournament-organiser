/*
A score_category is essentially a way to classify scores that might have to be
modified from their raw values. e.g. A battle score might be worth 60% of the
tournament points; A painting score might be ignored for determing matchups; etc.
*/

CREATE TABLE score_category(
    id                  SERIAL PRIMARY KEY,
    tournament_id       VARCHAR NOT NULL REFERENCES tournament(name),
    display_name        VARCHAR NOT NULL,
    percentage          INTEGER NOT NULL DEFAULT 100,
    per_tournament      BOOLEAN NOT NULL DEFAULT FALSE,
    min_val             INTEGER,
    max_val             INTEGER
);
COMMENT ON COLUMN score_category.percentage IS 'The raw score should be multiplied by this.';

CREATE TABLE score_key (
    id                  SERIAL UNIQUE,
    key                 VARCHAR NOT NULL,
    category            INTEGER NOT NULL REFERENCES score_category(id),
    PRIMARY KEY (key, category)
);
COMMENT ON TABLE score_key IS 'This table is all the score keys that might be entered for a tournament. An example might be round_1_battle, round_1_sports, best_painted_votes';

CREATE TABLE score (
    id                  SERIAL UNIQUE,
    entry_id            INTEGER REFERENCES entry(id),
    score_key_id        INTEGER REFERENCES score_key(id),
    value               INTEGER,
    PRIMARY KEY (entry_id, score_key_id)
);
COMMENT ON TABLE score IS 'An entry will have lots of scores.';

CREATE TABLE round_score(
    score_key_id        INTEGER REFERENCES score_key(id),
    round_id            INTEGER REFERENCES tournament_round(id)
);

CREATE TABLE game_score (
    entry_id    INTEGER REFERENCES entry(id),
    game_id     INTEGER REFERENCES game(id),
    score_id    INTEGER REFERENCES score(id),
    PRIMARY KEY (entry_id, game_id, score_id)
);
COMMENT ON TABLE game_score IS 'A score for a single game';
