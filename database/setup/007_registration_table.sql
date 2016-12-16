CREATE TABLE registration(
    player_id           VARCHAR REFERENCES account(username),
    tournament_id       INTEGER REFERENCES tournament(id),
    has_paid            boolean not null default False,
    turned_up           boolean not null default False,
    list_accept         boolean not null default False,
    PRIMARY KEY (player_id, tournament_id)
);
