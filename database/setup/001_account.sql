CREATE TABLE account(
    username            VARCHAR PRIMARY KEY,
    contact_email       varchar not null,
    is_superuser        BOOLEAN NOT NULL DEFAULT FALSE
);
