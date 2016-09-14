SELECT setup_permissions();

-- Set up some tournaments
INSERT INTO tournament VALUES (DEFAULT, 'northcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'southcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'conquest_2095', '2095-10-31');
INSERT INTO tournament VALUES (DEFAULT, 'empty_tournament', '2021-06-04');
INSERT INTO tournament VALUES (DEFAULT, 'rounds_test', '2021-06-04');

SELECT create_score_category('southcon_2095', 'some_category', 10, FALSE, 1, 10);
SELECT create_score_category('northcon_2095', 'leastnortherly', 10, FALSE, 1, 10);

SELECT create_user('charlie_murphy');

SELECT half_tournament_test_setup('ranking_test', '2095-08-12');
SELECT half_tournament_test_setup('enter_score_test', '2295-11-11');


-- Set up some users
DO $$
DECLARE
    fanciness int := 0;
    protect_object_id int := 0;
    tourn_id int := 0;
    tourn_name varchar := 'painting_test';
BEGIN
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-10-10', DEFAULT, protect_object_id) RETURNING id INTO tourn_id;
    fanciness = create_score_category(tourn_name, 'Fanciness', 10, TRUE, 4, 15);

    PERFORM add_player(tourn_name, tourn_id, 'stevemcqueen');
    PERFORM add_player(tourn_name, tourn_id, 'rick_james');
END $$;

-- Make a tournament for the purposes of testing missions
DO $$
DECLARE
    tourn_name varchar := 'mission_test';
    protect_object_id int := 0;
BEGIN
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-12', 3, protect_object_id);
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 1, 'Mission the First');
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 2, 'Mission the Second');
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 3, 'Mission the Third');
END $$;

-- Make a tournament for the purposes of testing categories
DO $$
DECLARE
    tourn_name varchar := 'category_test';
BEGIN
    PERFORM create_tournament(tourn_name, '2095-07-12');
    PERFORM create_score_category(tourn_name, 'category_1', 15, FALSE, 1, 10);
END $$;

-- Make a tournament for the purposes of testing permissions
DO $$
DECLARE
    tourn_name varchar := 'permission_test';
    tourn_id int := 0;
    protect_object_id int := 0;
    protected_object_action_id int := 0;
    protected_object_permission_id int := 0;
    username varchar := '';
BEGIN
    -- Create a superuser
    PERFORM create_user('superman', TRUE);

    -- Create a tournament that will be restricted
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-12', DEFAULT, protect_object_id) RETURNING id INTO tourn_id;

    -- Create a user with access to modify
    PERFORM create_user('lex_luthor');

    -- Give them permission to enter a score for it
    SELECT id INTO protected_object_action_id FROM protected_object_action WHERE description = 'enter_score' LIMIT 1;
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id, 
        (SELECT id FROM protected_object_action
            WHERE description = 'enter_score' LIMIT 1)
        ) RETURNING id INTO protected_object_permission_id;
    INSERT INTO account_protected_object_permission VALUES ('lex_luthor', protected_object_permission_id);

    -- Create a basic player
    PERFORM add_player(tourn_name, tourn_id, 'permission_test_player');
END $$;
