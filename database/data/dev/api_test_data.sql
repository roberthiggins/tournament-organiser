SELECT setup_permissions();

SELECT create_tournament('northcon_2095', '2095-06-01');

SELECT create_user('charlie_murphy');
SELECT create_user('superuser', TRUE);


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
    tourn varchar := 'permission_test';
    tourn_id int := 0;
BEGIN
    tourn_id := create_tournament(tourn, '2095-07-06');
    PERFORM add_player(tourn, tourn_id, 'permission_test_player');
END $$;


-- Tournament to test entering tournament-wide scores
DO $$
DECLARE
    tourn_id int := 0;
    tourn varchar := 'enter_score_test';
BEGIN
    -- Create a tournament that will be restricted
    tourn_id := create_tournament(tourn, '2095-10-10');

    PERFORM create_score_category(tourn, tourn || '_category_1', 1, TRUE, 4, 15);
    PERFORM create_score_category(tourn, tourn || '_category_2', 1, TRUE, 1, 5);
    PERFORM create_score_category(tourn, tourn || '_category_3', 1, TRUE, 1, 5);
    PERFORM create_score_category(tourn, tourn || '_category_su', 1, TRUE, 1, 5);
    PERFORM create_score_category(tourn, tourn || '_category_to', 1, TRUE, 1, 5);
    PERFORM create_score_category(tourn, tourn || '_category_per_game_1', 1, FALSE, 4, 15, TRUE);
    PERFORM create_score_category(tourn, tourn || '_category_per_game_2', 1, FALSE, 1, 5, TRUE);
    PERFORM create_score_category(tourn, tourn || '_category_per_game_3', 1, FALSE, 1, 5, TRUE);
    PERFORM create_score_category(tourn, tourn || '_category_per_game_4', 1, FALSE, 1, 5, TRUE);
    PERFORM create_score_category(tourn, tourn || '_category_per_game_su', 1, FALSE, 1, 5, TRUE);
    PERFORM create_score_category(tourn, tourn || '_category_per_game_to', 1, FALSE, 1, 5, TRUE);

    PERFORM add_player(tourn, tourn_id, tourn || '_p_1');
    PERFORM add_player(tourn, tourn_id, tourn || '_p_2');
END $$;


SELECT create_tournament('round_test', '2095-07-07');


SELECT half_tournament_test_setup('next_game_test', '2095-08-12');
SELECT half_tournament_test_setup('rank_test', '1643-01-27');
SELECT half_tournament_test_setup('schedule_test', '2163-09-15');
SELECT half_tournament_test_setup('draw_test', '1985-01-27');
