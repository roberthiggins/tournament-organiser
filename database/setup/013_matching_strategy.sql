CREATE TABLE matching_strategy(
    id VARCHAR PRIMARY KEY
);

CREATE TABLE tournament_matching_strategy(
    tournament_id     INTEGER NOT NULL REFERENCES tournament(id),
    matching_strategy VARCHAR NOT NULL REFERENCES matching_strategy(id)
);
