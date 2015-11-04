CREATE TABLE registration(
    player_id           VARCHAR REFERENCES player(username),
    tournament_id       VARCHAR REFERENCES tournament(name),
    PRIMARY KEY (player_id, tournament_id)
);
