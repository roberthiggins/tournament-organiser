/*
A score_category is essentially a way to classify scores that might have to be
modified from their raw values. e.g. A battle score might be worth 60% of the
tournament points; A painting score might be ignored for determing matchups; etc.
*/
CREATE TABLE score_category(
    id             SERIAL PRIMARY KEY,
    tournament_id  VARCHAR NOT NULL REFERENCES tournament(name),
    name           VARCHAR NOT NULL,
    percentage     INTEGER NOT NULL DEFAULT 100,
    per_tournament BOOLEAN NOT NULL DEFAULT FALSE,
    min_val        INTEGER,
    max_val        INTEGER,
    zero_sum       BOOLEAN NOT NULL DEFAULT FALSE
);
COMMENT ON COLUMN score_category.percentage IS 'The raw score should be multiplied by this.';

CREATE TABLE score (
    id                  SERIAL PRIMARY KEY,
    entry_id            INTEGER REFERENCES entry(id),
    score_category_id   INTEGER REFERENCES score_category(id),
    value               INTEGER
);
COMMENT ON TABLE score IS 'An entry will have lots of scores.';

CREATE TABLE game_score (
    entry_id    INTEGER REFERENCES entry(id),
    game_id     INTEGER REFERENCES game(id),
    score_id    INTEGER REFERENCES score(id),
    PRIMARY KEY (entry_id, game_id, score_id)
);
COMMENT ON TABLE game_score IS 'A score for a single game';

CREATE TABLE tournament_score (
    entry_id            INTEGER REFERENCES entry(id),
    tournament_id       INTEGER REFERENCES tournament(id),
    score_id            INTEGER REFERENCES score(id),
    PRIMARY KEY (entry_id, tournament_id, score_id)
);
COMMENT ON TABLE tournament_score IS 'A one-off score for a tournament';
