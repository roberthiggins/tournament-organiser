-- Tournament Round. The purpose of this is to store the ordering of rounds,
-- the mission, all the score keys that are needed for this round.

CREATE TABLE tournament_round(
    id                  SERIAL UNIQUE,
    tournament_name     VARCHAR REFERENCES tournament(name),
    ordering            INTEGER DEFAULT 1,
    mission             VARCHAR NOT NULL DEFAULT 'TBA',
    PRIMARY KEY(tournament_name, ordering)
);
COMMENT ON TABLE tournament_round IS 'The higher the order number the later the round.';
