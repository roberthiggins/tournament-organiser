create table entry (
        id 		serial not null primary key,
        player_id       varchar REFERENCES player(username),
        tournament_id   varchar references tournament(name)
);
