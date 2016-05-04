create table game(
    id                  serial unique PRIMARY KEY,
    tournament_round_id integer NOT NULL references tournament_round(id),
    table_num           integer,
    protected_object_id integer references protected_object(id),
    score_entered       boolean DEFAULT False
);

CREATE TABLE game_entrant(
    game_id INTEGER REFERENCES game(id),
    entrant_id INTEGER REFERENCES entry(id),
    PRIMARY KEY(game_id, entrant_id)
);
