CREATE TABLE player (
    username    varchar NOT NULL UNIQUE references account(username),
    settings    json
);
