create table entry (
        id 		serial not null primary key,
        player_id       varchar REFERENCES account(username),
        tournament_id   varchar references tournament(name)
);
