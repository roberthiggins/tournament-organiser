CREATE TABLE account(
    username      VARCHAR PRIMARY KEY,
    contact_email VARCHAR NOT NULL,
    first_name    VARCHAR NOT NULL DEFAULT '',
    last_name     VARCHAR NOT NULL DEFAULT '',
    is_superuser  BOOLEAN NOT NULL DEFAULT FALSE
);
