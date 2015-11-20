CREATE TABLE registration(
    player_id           VARCHAR REFERENCES player(username),
    tournament_id       VARCHAR REFERENCES tournament(name),
    has_paid		boolean not null,
    turned_up		boolean not null,
    list_accept		boolean not null,
    PRIMARY KEY (player_id, tournament_id)
);
