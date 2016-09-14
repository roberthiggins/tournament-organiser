SELECT setup_permissions();

INSERT INTO tournament VALUES (DEFAULT, 'northcon_2095', '2095-06-01');

SELECT create_user('charlie_murphy');


-- Make a tournament for the purposes of testing missions
DO $$
DECLARE
    tourn_name varchar := 'mission_test';
BEGIN
    PERFORM create_tournament(tourn_name, '2095-07-01');
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 1, 'Mission the First');
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 2, 'Mission the Second');
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 3, 'Mission the Third');
END $$;


-- Make a tournament for the purposes of testing entry info
DO $$
DECLARE
    tourn_name varchar := 'entry_info_test';
    tourn_id int := 0;
BEGIN
    tourn_id := create_tournament(tourn_name, '2095-07-02');
    PERFORM add_player(tourn_name, tourn_id, 'entry_info_player');
END $$;


-- Make a tournament for the purposes of testing entry lists
DO $$
DECLARE
    tourn_name varchar := 'entry_list_test';
    tourn_id int := 0;
BEGIN

    -- Create a tournament that will be restricted
    tourn_id := create_tournament(tourn_name, '2095-07-03');
    PERFORM add_player(tourn_name, tourn_id, 'entry_list_player');
    PERFORM add_player(tourn_name, tourn_id, 'entry_list_player_2');

    PERFORM create_tournament('entry_list_test_no_entries', '2095-07-04');
END $$;


-- Make a tournament for the purposes of testing categories
DO $$
DECLARE
    tourn_name varchar := 'category_test';
BEGIN
    PERFORM create_tournament(tourn_name, '2095-07-05');
    PERFORM create_score_category(tourn_name, 'category_1', 15, FALSE, 1, 10, TRUE);
END $$;


-- Make a tournament for the purposes of testing permissions
DO $$
DECLARE
    tourn_name varchar := 'permission_test';
    tourn_id int := 0;
BEGIN
    tourn_id := create_tournament(tourn_name, '2095-07-06');
    PERFORM add_player(tourn_name, tourn_id, 'permission_test_player');
END $$;


-- Tournament to test entering tournament-wide scores
DO $$
DECLARE
    protect_object_id int := 0;
    tourn_id int := 0;
    tourn_name varchar := 'enter_score_test';
    protected_object_action_id int := 0;
    protected_object_permission_id int := 0;
BEGIN
    -- Create a superuser
    PERFORM create_user('superuser', TRUE);

    -- Create a tournament that will be restricted
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-10-10', DEFAULT, protect_object_id) RETURNING id INTO tourn_id;

    PERFORM create_score_category(tourn_name, 'enter_score_test_category_1', 1, TRUE, 4, 15);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_2', 1, TRUE, 1, 5);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_3', 1, TRUE, 1, 5);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_su', 1, TRUE, 1, 5);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_to', 1, TRUE, 1, 5);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_per_game_1', 1, FALSE, 4, 15, TRUE);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_per_game_2', 1, FALSE, 1, 5, TRUE);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_per_game_3', 1, FALSE, 1, 5, TRUE);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_per_game_4', 1, FALSE, 1, 5, TRUE);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_per_game_su', 1, FALSE, 1, 5, TRUE);
    PERFORM create_score_category(tourn_name, 'enter_score_test_category_per_game_to', 1, FALSE, 1, 5, TRUE);

    -- Create a tournament organiser
    PERFORM create_user('to');

    -- Give them permission to enter a score for it
    SELECT id INTO protected_object_action_id FROM protected_object_action WHERE description = 'enter_score' LIMIT 1;
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id, 
        (SELECT id FROM protected_object_action
            WHERE description = 'enter_score' LIMIT 1)
        ) RETURNING id INTO protected_object_permission_id;
    INSERT INTO account_protected_object_permission VALUES ('to', protected_object_permission_id);

    PERFORM add_player(tourn_name, tourn_id, 'enter_score_test_p_1');
    PERFORM add_player(tourn_name, tourn_id, 'enter_score_test_p_2');
END $$;


SELECT create_tournament('round_test', '2095-07-07');


SELECT half_tournament_test_setup('next_game_test', '2095-08-12');
SELECT half_tournament_test_setup('rank_test', '1643-01-27');
SELECT half_tournament_test_setup('schedule_test', '2163-09-15');
SELECT half_tournament_test_setup('draw_test', '1985-01-27');
