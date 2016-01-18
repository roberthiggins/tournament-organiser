create table organiser (
	id integer references account(id),
	username varchar not null unique,
	settings json
);

CREATE VIEW tournament_organiser_permissions AS
    SELECT
        t.name          AS tournament_name,
        t.id            AS tournament_id,
        a.id            AS account_id,
        o.username,
        poa.description AS permission_description
    FROM        tournament                              t
    INNER JOIN  protected_object                        po
        ON t.protected_object_id = po.id
    INNER JOIN  protected_object_permission             pop
        ON po.id = pop.protected_object_id
    INNER JOIN protected_object_action                  poa
        ON poa.id = pop.protected_object_action_id
    INNER JOIN  account_protected_object_permission     apop
        ON apop.protected_object_permission_id = pop.id
    INNER JOIN  account                                 a
        ON a.id = apop.account_id
    INNER JOIN  organiser                               o
        ON a.id = o.id
;
