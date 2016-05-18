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
