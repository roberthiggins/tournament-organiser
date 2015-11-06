CREATE TABLE account_security (
    id          integer references account(id),
    password    varchar not null
);
