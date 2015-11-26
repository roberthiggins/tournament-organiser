create table entry (
        id 		serial not null unique primary key,
        player_id       varchar REFERENCES player(username),
        tournament_id   varchar unique references tournament(name)
);
