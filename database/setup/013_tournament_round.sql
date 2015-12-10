-- Tournament Round. The purpose of this is to store the ordering of rounds,
-- the mission, all the score keys that are needed for this round.

CREATE TABLE tournament_round(
    id                  SERIAL PRIMARY KEY,
    tournament_id       VARCHAR NOT NULL REFERENCES tournament(name),
    ordering            INTEGER NOT NULL DEFAULT 1
);
COMMENT ON TABLE tournament_round IS 'The higher the order number the later the round.';

CREATE TABLE round_score(
    score_key_id        INTEGER REFERENCES score_key(id),
    round_id            INTEGER REFERENCES tournament_round(id)
);
