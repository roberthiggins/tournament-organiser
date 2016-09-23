CREATE TABLE tournament(
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR NOT NULL UNIQUE,
    date                DATE NOT NULL,
    num_rounds	        INTEGER DEFAULT 0,
    protected_object_id INTEGER NOT NULL REFERENCES protected_object(id)
);
