CREATE TABLE tournament(
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR NOT NULL UNIQUE,
    date                DATE NOT NULL,
    protected_object_id INTEGER NOT NULL REFERENCES protected_object(id),
    creator_username    VARCHAR NOT NULL REFERENCES account(username)
);
