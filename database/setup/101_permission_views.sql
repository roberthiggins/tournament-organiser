CREATE VIEW tournament_organiser_permissions AS
    SELECT
        t.name          AS tournament_name,
        t.id            AS tournament_id,
        a.username,
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
        ON a.username = apop.account_username
;

CREATE VIEW game_permissions AS
    SELECT
        g.id            AS game_id,
        g.tourn         AS tournament_name,
        g.round_num     AS round_num,
        poa.description AS permission_description,
        a.username      AS username
    FROM game                                           g
    INNER JOIN  protected_object                        po
        ON g.protected_object_id = po.id
    INNER JOIN  protected_object_permission             pop
        ON po.id = pop.protected_object_id
    INNER JOIN protected_object_action                  poa
        ON poa.id = pop.protected_object_action_id
    INNER JOIN  account_protected_object_permission     apop
        ON apop.protected_object_permission_id = pop.id
    INNER JOIN  account                                 a
        ON a.username = apop.account_username
;
