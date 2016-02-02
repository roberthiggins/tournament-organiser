create table game(
    id                  serial unique,
    round_num           integer NOT NULL,
    tourn               varchar NOT NULL references tournament(name),
    table_num           integer,
    protected_object_id integer references protected_object(id),
    PRIMARY KEY(table_num, round_num, tourn)
);

CREATE TABLE game_entrant(
    game_id INTEGER REFERENCES game(id),
    entrant_id INTEGER REFERENCES entry(id),
    PRIMARY KEY(game_id, entrant_id)
);
