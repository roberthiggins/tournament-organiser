CREATE TABLE registration(
    player_id           VARCHAR REFERENCES player(username),
    tournament_id       VARCHAR REFERENCES tournament(name),
    has_paid            boolean not null default False,
    turned_up           boolean not null default False,
    list_accept         boolean not null default False,
    PRIMARY KEY (player_id, tournament_id)
);
