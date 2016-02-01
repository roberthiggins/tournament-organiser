create table game(
    id                  serial unique,
    entry_1             integer references entry(id) NOT NULL,
    entry_2             integer references entry(id),
    round_num           integer NOT NULL,
    tourn               varchar NOT NULL references tournament(name),
    table_num           integer,
    protected_object_id integer references protected_object(id),
    PRIMARY KEY(entry_1, round_num, tourn)
);
COMMENT ON TABLE game IS 'entry_2 is not needed in primary key as it may be null and the game should be unique with a single entry; An entry can only play in a single game.';
