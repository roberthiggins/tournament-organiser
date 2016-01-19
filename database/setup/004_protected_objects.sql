/*
    Objects are protected with an ACL (access control list) pattern.

    If you want to control who can enter a game score for a tournament you
    might do the following:
        - add an entry to the protected_object table.
        - reference this from the tournament table. Permissions can now be
          added to that tournament.
        - Create a row in protected_object_action called 'enter_game_score' (if
          a suitable action didn't exist already)
        - Create a row in protected_object_permission that references
          protected_object_action and protected_object. This is essentially an
          instance object representing permission to 'enter_game_score' for
          your tournament.
        - Create a row in account_protected_object_permission to link an
          account with the protected_object_permission row above.
*/
CREATE TABLE protected_object(
    id SERIAL PRIMARY KEY
);
COMMENT ON TABLE protected_object IS 'A list of objects on which restrictions can be placed. Most/all tournaments should reference this for example.';


CREATE TABLE protected_object_action(
    id          SERIAL PRIMARY KEY,
    description VARCHAR NOT NULL
);
COMMENT ON TABLE protected_object_action IS 'An abstract action that could be performed on a protected_object. "Enter Score", "add player", etc.';


CREATE TABLE protected_object_permission(
    id                          SERIAL UNIQUE,
    protected_object_id         INTEGER REFERENCES protected_object(id),
    protected_object_action_id  INTEGER REFERENCES protected_object_action(id),
    PRIMARY KEY(protected_object_id, protected_object_action_id)
);
COMMENT ON TABLE protected_object_permission IS 'An instance of a protected_object_action on a protected object e.g. enter score for tournament #2';

CREATE TABLE account_protected_object_permission(
    account_username                    VARCHAR REFERENCES account(username),
    protected_object_permission_id      INTEGER REFERENCES protected_object_permission(id),
    PRIMARY KEY(account_username, protected_object_permission_id)
);
COMMENT ON TABLE account_protected_object_permission IS 'Links instance permissions to accounts';
