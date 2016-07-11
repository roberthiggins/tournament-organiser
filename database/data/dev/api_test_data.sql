INSERT INTO protected_object_action VALUES (DEFAULT, 'enter_score');

INSERT INTO tournament VALUES (DEFAULT, 'northcon_2095', '2095-06-01');

INSERT INTO account VALUES ('charlie_murphy', 'charlie_murphy@darkness.com');
INSERT INTO account_security VALUES ('charlie_murphy', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');

-- Create player and enter them in to a tournament
CREATE OR REPLACE FUNCTION add_player(tourn_name varchar, tourn_id int, player_name varchar) RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    entry_id int := 0;
BEGIN

    INSERT INTO account VALUES (player_name, 'foo@bar.com') ;
    INSERT INTO account_security VALUES (player_name, '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');
    INSERT INTO registration VALUES(player_name, tourn_id);
    INSERT INTO entry VALUES(default, player_name, tourn_name) RETURNING id INTO entry_id;

    RETURN entry_id;
END $$;


-- Make a tournament for the purposes of testing missions
CREATE OR REPLACE FUNCTION mission_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_name varchar := 'mission_test';
    protect_object_id int := 0;
BEGIN

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-01', 3, protect_object_id);
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 1, 'Mission the First');
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 2, 'Mission the Second');
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 3, 'Mission the Third');

    RETURN 0;
END $$;
SELECT mission_test_setup();

-- Make a tournament for the purposes of testing entry info
CREATE OR REPLACE FUNCTION entry_info_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_name varchar := 'entry_info_test';
    tourn_id int := 0;
    protect_object_id int := 0;
BEGIN

    -- Create a tournament that will be restricted
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-02', DEFAULT, protect_object_id) RETURNING id INTO tourn_id;

    PERFORM add_player(tourn_name, tourn_id, 'entry_info_player');

    RETURN 0;
END $$;
SELECT entry_info_test_setup();

-- Make a tournament for the purposes of testing entry lists
CREATE OR REPLACE FUNCTION entry_list_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_name varchar := 'entry_list_test';
    tourn_id int := 0;
    protect_object_id int := 0;
BEGIN

    -- Create a tournament that will be restricted
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-03', DEFAULT, protect_object_id) RETURNING id INTO tourn_id;

    PERFORM add_player(tourn_name, tourn_id, 'entry_list_player');
    PERFORM add_player(tourn_name, tourn_id, 'entry_list_player_2');

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, 'entry_list_test_no_entries', '2095-07-04', DEFAULT, protect_object_id);

    RETURN 0;
END $$;
SELECT entry_list_test_setup();


-- Make a tournament for the purposes of testing categories
CREATE OR REPLACE FUNCTION category_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_name varchar := 'category_test';
    protect_object_id int := 0;
BEGIN

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-05', 3, protect_object_id);
    INSERT INTO score_category VALUES(DEFAULT, tourn_name, 'category_1', 15, DEFAULT, 1, 10);

    RETURN 0;
END $$;
SELECT category_test_setup();

-- Make a tournament for the purposes of testing permissions
CREATE OR REPLACE FUNCTION permission_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_name varchar := 'permission_test';
    tourn_id int := 0;
    protect_object_id int := 0;
BEGIN

    -- Create a tournament that will be restricted
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-06', DEFAULT, protect_object_id) RETURNING id INTO tourn_id;

    PERFORM add_player(tourn_name, tourn_id, 'permission_test_player');

    RETURN 0;
END $$;
SELECT permission_test_setup();

-- Make a tournament for the purposes of testing rounds
CREATE OR REPLACE FUNCTION round_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_name varchar := 'round_test';
    protect_object_id int := 0;
BEGIN

    -- Create a tournament that will be restricted
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-07', DEFAULT, protect_object_id);

    RETURN 0;
END $$;
SELECT round_test_setup();

-- Make game
CREATE OR REPLACE FUNCTION make_game(round_id int, table_num int, ent_1_id int, ent_1_uname varchar, ent_2_id int, ent_2_uname varchar,  prot_act_id int ) RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    prot_obj_id int := 0;
    game_id int := 0;
    perm_id int := 0;
BEGIN
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO prot_obj_id;
    INSERT INTO game VALUES(DEFAULT, round_id, table_num, prot_obj_id, True) RETURNING id INTO game_id;
    INSERT INTO protected_object_permission VALUES (DEFAULT, prot_obj_id, prot_act_id) RETURNING id INTO perm_id;

    IF ent_1_id IS NOT NULL AND ent_1_uname IS NOT NULL THEN
        INSERT INTO game_entrant VALUES(game_id, ent_1_id);
        INSERT INTO account_protected_object_permission VALUES (ent_1_uname, perm_id);
    END IF;

    IF ent_2_id IS NOT NULL AND ent_2_uname IS NOT NULL THEN
        INSERT INTO game_entrant VALUES(game_id, ent_2_id);
        INSERT INTO account_protected_object_permission VALUES (ent_2_uname, perm_id);
    END IF;

    RETURN game_id;
END $$;

-- Enter score for player
CREATE OR REPLACE FUNCTION enter_score(game_id int, ent_id int, category int, score int) RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    score_id int := 0;
BEGIN
    INSERT INTO score VALUES(DEFAULT, ent_id, category, score) RETURNING id INTO score_id;
    INSERT INTO game_score VALUES(ent_id, game_id, score_id);

    RETURN 0;
END $$;


-- Make a partially complete tournament
CREATE OR REPLACE FUNCTION half_tournament_test_setup(tourn_name varchar, tourn_date date) RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    cat_1 int := 0;
    cat_2 int := 0;
    prot_obj_id int := 0;
    prot_act_id int := 0;
    perm_id int := 0;
    game_id int := 0;
    round_1_id int := 0;
    round_2_id int := 0;
    tourn_id int := 0;
    ent_1_id int := 0;
    ent_2_id int := 0;
    ent_3_id int := 0;
    ent_4_id int := 0;
    ent_5_id int := 0;
BEGIN

    INSERT INTO protected_object VALUES(DEFAULT)                                               RETURNING id INTO prot_obj_id;
    INSERT INTO tournament       VALUES(DEFAULT, tourn_name, tourn_date, DEFAULT, prot_obj_id) RETURNING id INTO tourn_id;
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 1, 'Kill')                        RETURNING id INTO round_1_id;
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 2, DEFAULT)                       RETURNING id INTO round_2_id;
    INSERT INTO score_category   VALUES(DEFAULT, tourn_name, 'Battle', 90, DEFAULT, 0, 20)     RETURNING id INTO cat_1;
    INSERT INTO score_category   VALUES(DEFAULT, tourn_name, 'Fair Play', 10, DEFAULT, 1, 5)   RETURNING id INTO cat_2;

    ent_1_id := add_player(tourn_name, tourn_id, tourn_name || '_player_1');
    INSERT INTO table_allocation VALUES(ent_1_id, 1, 1);
    INSERT INTO table_allocation VALUES(ent_1_id, 2, 2);

    ent_2_id := add_player(tourn_name, tourn_id, tourn_name || '_player_2');
    INSERT INTO table_allocation VALUES(ent_2_id, 2, 1);

    ent_3_id := add_player(tourn_name, tourn_id, tourn_name || '_player_3');
    INSERT INTO table_allocation VALUES(ent_3_id, 2, 2);

    ent_4_id := add_player(tourn_name, tourn_id, tourn_name || '_player_4');
    INSERT INTO table_allocation VALUES(ent_4_id, 2, 1);
    INSERT INTO table_allocation VALUES(ent_4_id, 1, 2);

    ent_5_id := add_player(tourn_name, tourn_id, tourn_name || '_player_5');
    INSERT INTO table_allocation VALUES(ent_5_id, 1, 1);
    INSERT INTO table_allocation VALUES(ent_5_id, 1, 2);

    -- The draw for round 1 has already been completed.
    SELECT id INTO prot_act_id FROM protected_object_action WHERE description = 'enter_score';

    game_id := make_game(round_1_id, 1, ent_3_id, tourn_name || '_player_3', NULL, NULL,  prot_act_id);

    game_id := make_game(round_1_id, 2, ent_1_id, tourn_name || '_player_1', ent_5_id, tourn_name || '_player_5',  prot_act_id);
    PERFORM enter_score(game_id, ent_1_id, cat_1, 20);
    PERFORM enter_score(game_id, ent_1_id, cat_2, 1);
    PERFORM enter_score(game_id, ent_5_id, cat_1, 0);
    PERFORM enter_score(game_id, ent_5_id, cat_2, 5);

    game_id := make_game(round_1_id, 3, ent_2_id, tourn_name || '_player_2', ent_4_id, tourn_name || '_player_4',  prot_act_id);
    PERFORM enter_score(game_id, ent_2_id, cat_1, 0);
    PERFORM enter_score(game_id, ent_2_id, cat_2, 5);
    PERFORM enter_score(game_id, ent_4_id, cat_1, 20);
    PERFORM enter_score(game_id, ent_4_id, cat_2, 5);

    -- The draw for round 2 has already been completed.
    SELECT id INTO prot_act_id FROM protected_object_action WHERE description = 'enter_score';

    game_id := make_game(round_2_id, 1, ent_2_id, tourn_name || '_player_2', NULL, NULL,  prot_act_id);

    game_id := make_game(round_2_id, 2, ent_5_id, tourn_name || '_player_5', ent_4_id, tourn_name || '_player_4',  prot_act_id);
    PERFORM enter_score(game_id, ent_4_id, cat_1, 5);
    PERFORM enter_score(game_id, ent_4_id, cat_2, 5);
--    PERFORM enter_score(game_id, ent_5_id, cat_1, 15);
--    PERFORM enter_score(game_id, ent_5_id, cat_2, 5);

    game_id := make_game(round_2_id, 3, ent_1_id, tourn_name || '_player_1', ent_3_id, tourn_name || '_player_3',  prot_act_id);
    PERFORM enter_score(game_id, ent_1_id, cat_1, 15);
    PERFORM enter_score(game_id, ent_1_id, cat_2, 5);
    PERFORM enter_score(game_id, ent_3_id, cat_1, 5);
    PERFORM enter_score(game_id, ent_3_id, cat_2, 5);

    RETURN 0;
END $$;
SELECT half_tournament_test_setup('next_game_test', '2095-08-12');
SELECT half_tournament_test_setup('rank_test', '1643-01-27');
SELECT half_tournament_test_setup('schedule_test', '2163-09-15');
