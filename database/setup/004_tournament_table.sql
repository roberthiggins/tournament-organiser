CREATE TABLE tournament(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR UNIQUE,
    date        DATE NOT NULL
);
