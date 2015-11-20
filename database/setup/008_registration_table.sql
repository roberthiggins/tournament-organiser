CREATE TABLE registration(
    player_id           VARCHAR REFERENCES player(username),
    tournament_id       VARCHAR REFERENCES tournament(name),
    PRIMARY KEY (player_id, tournament_id),
	has_paid			bool not null,
	turned_up			bool not null,
	list_accept			bool not null
);
