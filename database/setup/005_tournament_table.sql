CREATE TABLE tournament(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR UNIQUE,
    date        DATE NOT NULL,
    num_rounds	INTEGER DEFAULT 0,
    score_id	integer references scoring(id)
);
