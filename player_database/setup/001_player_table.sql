CREATE TABLE player (
    id serial primary key,
    username varchar not null  unique,
    settings json
);
