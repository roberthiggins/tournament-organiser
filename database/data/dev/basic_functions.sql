-- Set up a user to be logged in
CREATE OR REPLACE FUNCTION create_user(username varchar, superuser boolean DEFAULT FALSE, first_name varchar DEFAULT '', last_name varchar DEFAULT '') RETURNS int LANGUAGE plpgsql AS $$
BEGIN

    INSERT INTO account VALUES (username, username || '@bar.com', first_name, last_name, superuser);
    INSERT INTO account_security VALUES (username, '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');

    RETURN 0;
END $$;

-- Set Up Permissions
CREATE OR REPLACE FUNCTION setup_permissions() RETURNS int LANGUAGE plpgsql AS $$
BEGIN

    INSERT INTO protected_object_action VALUES (DEFAULT, 'enter_score');
    INSERT INTO protected_object_action VALUES (DEFAULT, 'modify_application');
    INSERT INTO protected_object_action VALUES (DEFAULT, 'modify_tournament');

    RETURN 0;
END $$;

-- Create TO for tourament
CREATE OR REPLACE FUNCTION create_to(tourn_name varchar, protect_object_id integer) RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    username varchar := tourn_name || '_to';
    protected_object_action_id int := 0;
    protected_object_permission_id int := 0;
BEGIN

    PERFORM create_user(username);

    SELECT id INTO protected_object_action_id FROM protected_object_action WHERE description = 'enter_score' LIMIT 1;
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id,
        (SELECT id FROM protected_object_action
            WHERE description = 'enter_score' LIMIT 1)
        ) RETURNING id INTO protected_object_permission_id;
    INSERT INTO account_protected_object_permission VALUES (username, protected_object_permission_id);

    SELECT id INTO protected_object_action_id FROM protected_object_action WHERE description = 'modify_tournament' LIMIT 1;
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id,
        (SELECT id FROM protected_object_action
            WHERE description = 'modify_tournament' LIMIT 1)
        ) RETURNING id INTO protected_object_permission_id;
    INSERT INTO account_protected_object_permission VALUES (username, protected_object_permission_id);

    RETURN 0;

END $$;


-- Make a tournament
CREATE OR REPLACE FUNCTION create_tournament(tourn_name varchar, tourn_date varchar) RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_id int := 0;
    protect_object_id int := 0;
BEGIN

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    PERFORM create_to(tourn_name, protect_object_id);

    INSERT INTO tournament VALUES (DEFAULT, tourn_name, cast(tourn_date AS date), protect_object_id, tourn_name || '_to') RETURNING id INTO tourn_id;

    RETURN tourn_id;
END $$;

-- Create player and enter them in to a tournament
CREATE OR REPLACE FUNCTION add_player(tourn_name varchar, tourn_id int, player_name varchar, first_name varchar DEFAULT '', last_name varchar DEFAULT '') RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    entry_id int := 0;
BEGIN

    PERFORM create_user(player_name, FALSE, first_name, last_name);
    INSERT INTO registration VALUES(player_name, tourn_id);
    INSERT INTO entry VALUES(default, player_name, tourn_name) RETURNING id INTO entry_id;

    RETURN entry_id;
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


-- Make game
CREATE OR REPLACE FUNCTION make_game(round_id int, table_num int, ent_1_id int, ent_1_uname varchar, ent_2_id int, ent_2_uname varchar,  prot_act_id int ) RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    prot_obj_id int := 0;
    game_id int := 0;
    perm_id int := 0;
    bye boolean := true;
BEGIN

    IF ent_1_id IS NOT NULL AND ent_1_uname IS NOT NULL AND ent_2_id IS NOT NULL AND ent_2_uname IS NOT NULL THEN
        bye = false;
    END IF;

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO prot_obj_id;
    INSERT INTO game VALUES(DEFAULT, round_id, table_num, prot_obj_id, bye) RETURNING id INTO game_id;
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

-- Make a score_category
CREATE OR REPLACE FUNCTION create_score_category(tourn_name varchar, name varchar, percentage integer, per_tourn boolean DEFAULT FALSE, min_val integer DEFAULT 1, max_val integer DEFAULT 20, zero_sum boolean DEFAULT FALSE, opponent_score boolean DEFAULT FALSE) RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    cat_1 int := 0;
BEGIN
    INSERT INTO score_category VALUES(DEFAULT, tourn_name, name, percentage, per_tourn, min_val, max_val, zero_sum, opponent_score) RETURNING id INTO cat_1;

    return cat_1;
END $$;

-- Make a partially complete tournament
CREATE OR REPLACE FUNCTION half_tournament_test_setup(tourn_name varchar, tourn_date varchar) RETURNS int LANGUAGE plpgsql AS $$
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
    ent_1_name varchar := tourn_name || '_player_1';
    ent_2_id int := 0;
    ent_2_name varchar := tourn_name || '_player_2';
    ent_3_id int := 0;
    ent_3_name varchar := tourn_name || '_player_3';
    ent_4_id int := 0;
    ent_4_name varchar := tourn_name || '_player_4';
    ent_5_id int := 0;
    ent_5_name varchar := tourn_name || '_player_5';
BEGIN

    tourn_id := create_tournament(tourn_name, tourn_date);
    UPDATE tournament SET in_progress = TRUE WHERE id = tourn_id;

    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 1, 'Kill')                        RETURNING id INTO round_1_id;
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 2, DEFAULT)                       RETURNING id INTO round_2_id;

    cat_1 = create_score_category(tourn_name, 'Battle', 90, FALSE, 0, 20, TRUE);
    cat_2 = create_score_category(tourn_name, 'Fair Play', 10, FALSE, 1, 5, FALSE, TRUE);

    ent_1_id := add_player(tourn_name, tourn_id, ent_1_name, tourn_name, 'P1');
    INSERT INTO table_allocation VALUES(ent_1_id, 1, 1);
    INSERT INTO table_allocation VALUES(ent_1_id, 2, 2);

    ent_2_id := add_player(tourn_name, tourn_id, ent_2_name);
    INSERT INTO table_allocation VALUES(ent_2_id, 2, 1);

    ent_3_id := add_player(tourn_name, tourn_id, ent_3_name);
    INSERT INTO table_allocation VALUES(ent_3_id, 2, 2);

    ent_4_id := add_player(tourn_name, tourn_id, ent_4_name);
    INSERT INTO table_allocation VALUES(ent_4_id, 2, 1);
    INSERT INTO table_allocation VALUES(ent_4_id, 1, 2);

    ent_5_id := add_player(tourn_name, tourn_id, ent_5_name);
    INSERT INTO table_allocation VALUES(ent_5_id, 1, 1);
    INSERT INTO table_allocation VALUES(ent_5_id, 1, 2);

    -- The draw for round 1 has already been completed.
    SELECT id INTO prot_act_id FROM protected_object_action WHERE description = 'enter_score';

    game_id := make_game(round_1_id, 1, ent_3_id, ent_3_name, NULL, NULL,  prot_act_id);

    game_id := make_game(round_1_id, 2, ent_1_id, ent_1_name, ent_5_id, ent_5_name,  prot_act_id);
    PERFORM enter_score(game_id, ent_1_id, cat_1, 20);
    PERFORM enter_score(game_id, ent_1_id, cat_2, 1);
    PERFORM enter_score(game_id, ent_5_id, cat_1, 0);
    PERFORM enter_score(game_id, ent_5_id, cat_2, 5);

    game_id := make_game(round_1_id, 3, ent_2_id, ent_2_name, ent_4_id, ent_4_name,  prot_act_id);
    PERFORM enter_score(game_id, ent_2_id, cat_1, 0);
    PERFORM enter_score(game_id, ent_2_id, cat_2, 5);
    PERFORM enter_score(game_id, ent_4_id, cat_1, 20);
    PERFORM enter_score(game_id, ent_4_id, cat_2, 5);

    -- The draw for round 2 has already been completed.
    SELECT id INTO prot_act_id FROM protected_object_action WHERE description = 'enter_score';

    game_id := make_game(round_2_id, 1, ent_2_id, ent_2_name, NULL, NULL,  prot_act_id);

    game_id := make_game(round_2_id, 2, ent_5_id, ent_5_name, ent_4_id, ent_4_name,  prot_act_id);
    PERFORM enter_score(game_id, ent_4_id, cat_1, 5);
    PERFORM enter_score(game_id, ent_4_id, cat_2, 5);
--    PERFORM enter_score(game_id, ent_5_id, cat_1, 15);
--    PERFORM enter_score(game_id, ent_5_id, cat_2, 5);

    game_id := make_game(round_2_id, 3, ent_1_id, ent_1_name, ent_3_id, ent_3_name,  prot_act_id);
    PERFORM enter_score(game_id, ent_1_id, cat_1, 15);
    PERFORM enter_score(game_id, ent_1_id, cat_2, 5);
    PERFORM enter_score(game_id, ent_3_id, cat_1, 5);
    PERFORM enter_score(game_id, ent_3_id, cat_2, 5);

    RETURN 0;
END $$;
