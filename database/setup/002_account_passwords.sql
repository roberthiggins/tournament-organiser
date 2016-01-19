CREATE TABLE account_security (
    id          varchar references account(username),
    password    varchar not null
);
