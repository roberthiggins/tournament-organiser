SELECT setup_permissions();
-- Create a superuser
SELECT create_user('superman', TRUE);

-- Set up some tournaments
SELECT create_tournament('empty_tournament', '2021-06-04');
SELECT create_tournament('rounds_test', '2021-06-04');

SELECT create_user('charlie_murphy');

SELECT half_tournament_test_setup('ranking_test', '2095-08-12');
SELECT half_tournament_test_setup('enter_score_test', '2295-11-11');
SELECT half_tournament_test_setup('next_game_test', '2395-11-11');


DO $$
DECLARE
    tourn_id int := 0;
    tourn_name varchar := 'tourn_score_test';
BEGIN
    tourn_id := create_tournament(tourn_name, '2095-10-10');
    UPDATE tournament SET in_progress = TRUE WHERE id = tourn_id;

    PERFORM create_score_category(tourn_name, 'Fanciness', 10, TRUE, 4, 15);
    PERFORM add_player(tourn_name, tourn_id, 'stevemcqueen');
    PERFORM add_player(tourn_name, tourn_id, 'rick_james');
END $$;

-- Make a tournament for the purposes of testing missions
DO $$
DECLARE
    tourn_name varchar := 'mission_test';
BEGIN
    PERFORM create_tournament(tourn_name, '2095-07-12');
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

-- Make a tournament for the purposes of testing entries
DO $$
DECLARE
    tourn_name varchar := 'entries_test';
    tourn_id int := 0;
BEGIN
    -- Create a tournament that will be restricted
    tourn_id := create_tournament(tourn_name, '3121-03-18');
    PERFORM add_player(tourn_name, tourn_id, tourn_name || '_p_1');
END $$;

-- Make a tournament for the purposes of testing withdrawals
DO $$
DECLARE
    tourn_name varchar := 'withdrawal_test';
    tourn_id int := 0;
BEGIN
    -- Create a tournament that will be restricted
    tourn_id := create_tournament(tourn_name, '3121-03-19');
    PERFORM add_player(tourn_name, tourn_id, tourn_name || '_p_1');
    PERFORM add_player(tourn_name, tourn_id, tourn_name || '_p_2');
END $$;

SELECT create_tournament('register_test_1', '2222-06-01');
SELECT create_tournament('register_test_2', '2222-06-02');
SELECT create_tournament('register_test_3', '2222-06-02');
SELECT create_user('register_test_player_1');
SELECT create_user('user_update_test');
