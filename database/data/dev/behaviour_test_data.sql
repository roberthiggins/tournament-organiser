-- Set up some tournaments
INSERT INTO tournament VALUES (DEFAULT, 'northcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'southcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'conquest_2095', '2095-10-31');

INSERT INTO score_category VALUES(DEFAULT, 'southcon_2095', 'some_category', DEFAULT);
INSERT INTO score_category VALUES(100, 'northcon_2095', 'leastnortherly', DEFAULT);

-- Set up some users
DO $$
DECLARE
    fanciness int := 0;
    protect_object_id int := 0;
    tournie_id int := 0;
BEGIN

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;

    INSERT INTO tournament VALUES (DEFAULT, 'painting_test', '2095-10-10', DEFAULT, protect_object_id) RETURNING id INTO tournie_id;

    INSERT INTO score_category VALUES(DEFAULT, 'painting_test', 'Fanciness', DEFAULT) RETURNING id INTO fanciness;
    INSERT INTO score_key VALUES (DEFAULT, 'fanciest_wig', 4, 15, fanciness);
    INSERT INTO score_key VALUES (DEFAULT, 'number_tassles', 2, 28, fanciness);

    INSERT INTO account VALUES ('stevemcqueen', 'foo@bar.com');
    INSERT INTO account_security VALUES ('stevemcqueen', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');
    INSERT INTO account VALUES ('rick_james', 'foo@bar.com');
    INSERT INTO account_security VALUES ('rick_james', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');
    INSERT INTO account VALUES ('charlie_murphy', 'chalie_murphy@darkness.com');
    INSERT INTO account_security VALUES ('charlie_murphy', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');

    -- Enter some players
    INSERT INTO registration VALUES('stevemcqueen', tournie_id);

    INSERT INTO entry VALUES(default, 'rick_james', 'painting_test');

END $$;

-- Make a tournament for the purposes of testing rankings
CREATE OR REPLACE FUNCTION ranking_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    eid int := 0;
    rd1key int := 0;
    rd2key int := 0;
    sportskey int := 0;
    battlecategory int := 0;
    sportscategory int := 0;
    protect_object_id int := 0;
    protected_action_id int := 0;
    permission_id int := 0;
    game_id int := 0;
    round_1_id int := 0;
    round_2_id int := 0;
    ranking_test_id int := 0;
BEGIN

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, 'ranking_test', '2095-08-12', DEFAULT, protect_object_id) RETURNING id INTO ranking_test_id;
    INSERT INTO tournament_round VALUES(DEFAULT, 'ranking_test', 1, 'Kill') RETURNING id INTO round_1_id;
    INSERT INTO tournament_round VALUES(DEFAULT, 'ranking_test', 2, DEFAULT) RETURNING id INTO round_2_id;

    INSERT INTO score_category VALUES(DEFAULT, 'ranking_test', 'Battle', 90) RETURNING id INTO battlecategory;
    INSERT INTO score_category VALUES(DEFAULT, 'ranking_test', 'Fair Play', 10) RETURNING id INTO sportscategory;
    INSERT INTO score_key VALUES (DEFAULT, 'round_1_battle', 0, 20, battlecategory) RETURNING id INTO rd1key;
    INSERT INTO score_key VALUES (DEFAULT, 'round_2_battle', 0, 20, battlecategory) RETURNING id INTO rd2key;
    INSERT INTO score_key VALUES (DEFAULT, 'sports', 1, 5, sportscategory) RETURNING id INTO sportskey;
    INSERT INTO round_score VALUES(rd1key, 1);
    INSERT INTO round_score VALUES(sportskey, 1);
    INSERT INTO round_score VALUES(rd2key, 2);

    INSERT INTO account VALUES ('homer', 'foo@bar.com') ;
    INSERT INTO account_security VALUES ('homer', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');
    INSERT INTO registration VALUES('homer', ranking_test_id);
    INSERT INTO entry VALUES(default, 'homer', 'ranking_test') RETURNING id INTO eid;
    INSERT INTO score VALUES(eid, rd1key, 20);
    INSERT INTO table_allocation VALUES(eid, 1, 1);
    INSERT INTO score VALUES(eid, rd2key, 15);
    INSERT INTO table_allocation VALUES(eid, 2, 2);
    INSERT INTO score VALUES(eid, sportskey, 1);


    INSERT INTO account VALUES ('marge', 'foo@bar.com') ;
    INSERT INTO account_security VALUES ('marge', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');
    INSERT INTO registration VALUES('marge', ranking_test_id);
    INSERT INTO entry VALUES(default, 'marge', 'ranking_test') RETURNING id INTO eid;
    INSERT INTO score VALUES(eid, rd1key, 0);
    INSERT INTO table_allocation VALUES(eid, 2, 1);
    INSERT INTO score VALUES(eid, rd2key, DEFAULT);
    INSERT INTO score VALUES(eid, sportskey, 5);

    INSERT INTO account VALUES ('lisa', 'foo@bar.com') ;
    INSERT INTO account_security VALUES ('lisa', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');
    INSERT INTO registration VALUES('lisa', ranking_test_id);
    INSERT INTO entry VALUES(default, 'lisa', 'ranking_test') RETURNING id INTO eid;
    INSERT INTO score VALUES(eid, rd1key, DEFAULT);
    INSERT INTO score VALUES(eid, rd2key, 5);
    INSERT INTO table_allocation VALUES(eid, 2, 2);
    INSERT INTO score VALUES(eid, sportskey, 5);

    INSERT INTO account VALUES ('bart', 'foo@bar.com') ;
    INSERT INTO account_security VALUES ('bart', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');
    INSERT INTO registration VALUES('bart', ranking_test_id);
    INSERT INTO entry VALUES(default, 'bart', 'ranking_test') RETURNING id INTO eid;
    INSERT INTO score VALUES(eid, rd1key, 0);
    INSERT INTO table_allocation VALUES(eid, 2, 1);
    INSERT INTO score VALUES(eid, rd2key, 5);
    INSERT INTO table_allocation VALUES(eid, 1, 2);
    INSERT INTO score VALUES(eid, sportskey, 5);

    INSERT INTO account VALUES ('maggie', 'foo@bar.com') ;
    INSERT INTO account_security VALUES ('maggie', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');
    INSERT INTO registration VALUES('maggie', ranking_test_id);
    INSERT INTO entry VALUES(default, 'maggie', 'ranking_test') RETURNING id INTO eid;
    INSERT INTO score VALUES(eid, rd1key, 0);
    INSERT INTO table_allocation VALUES(eid, 1, 1);
     --INSERT INTO score VALUES(eid, rd2key, 5);
    INSERT INTO table_allocation VALUES(eid, 1, 2);
    INSERT INTO score VALUES(eid, sportskey, 5);

    -- The draw for round 1 has already been completed.
    SELECT id INTO protected_action_id FROM protected_object_action WHERE description = 'enter_score';

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO game VALUES(DEFAULT, round_1_id, 1, protect_object_id) RETURNING id INTO game_id;
    INSERT INTO game_entrant VALUEs(game_id, 4);
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id, protected_action_id) RETURNING id INTO permission_id;
    INSERT INTO account_protected_object_permission VALUES ('lisa', permission_id);

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO game VALUES(DEFAULT, round_1_id, 2, protect_object_id, True) RETURNING id INTO game_id;
    INSERT INTO game_entrant VALUEs(game_id, 2);
    INSERT INTO game_entrant VALUEs(game_id, 6);
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id, protected_action_id) RETURNING id INTO permission_id;
    INSERT INTO account_protected_object_permission VALUES ('homer', permission_id);
    INSERT INTO account_protected_object_permission VALUES ('maggie', permission_id);

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO game VALUES(DEFAULT, round_1_id, 3, protect_object_id, True) RETURNING id INTO game_id;
    INSERT INTO game_entrant VALUEs(game_id, 3);
    INSERT INTO game_entrant VALUEs(game_id, 5);
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id, protected_action_id) RETURNING id INTO permission_id;
    INSERT INTO account_protected_object_permission VALUES ('marge', permission_id);
    INSERT INTO account_protected_object_permission VALUES ('bart', permission_id);

    -- The draw for round 2 has already been completed.
    SELECT id INTO protected_action_id FROM protected_object_action WHERE description = 'enter_score';

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO game VALUES(DEFAULT, round_2_id, 1, protect_object_id, True) RETURNING id INTO game_id;
    INSERT INTO game_entrant VALUEs(game_id, 3);
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id, protected_action_id) RETURNING id INTO permission_id;
    INSERT INTO account_protected_object_permission VALUES ('marge', permission_id);

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO game VALUES(DEFAULT, round_2_id, 2, protect_object_id) RETURNING id INTO game_id;
    INSERT INTO game_entrant VALUEs(game_id, 6);
    INSERT INTO game_entrant VALUEs(game_id, 5);
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id, protected_action_id) RETURNING id INTO permission_id;
    INSERT INTO account_protected_object_permission VALUES ('maggie', permission_id);
    INSERT INTO account_protected_object_permission VALUES ('bart', permission_id);

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO game VALUES(DEFAULT, round_2_id, 3, protect_object_id, True) RETURNING id INTO game_id;
    INSERT INTO game_entrant VALUEs(game_id, 2);
    INSERT INTO game_entrant VALUEs(game_id, 4);
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id, protected_action_id) RETURNING id INTO permission_id;
    INSERT INTO account_protected_object_permission VALUES ('homer', permission_id);
    INSERT INTO account_protected_object_permission VALUES ('lisa', permission_id);


    RETURN 0;
END $$;
SELECT ranking_test_setup();

-- Make a tournament for the purposes of testing missions
CREATE OR REPLACE FUNCTION mission_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_name varchar := 'mission_test';
    protect_object_id int := 0;
BEGIN

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-12', 3, protect_object_id);
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 1, 'Mission the First');
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 2, 'Mission the Second');
    INSERT INTO tournament_round VALUES(DEFAULT, tourn_name, 3, 'Mission the Third');

    RETURN 0;
END $$;
SELECT mission_test_setup();

-- Make a tournament for the purposes of testing categories
CREATE OR REPLACE FUNCTION category_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_name varchar := 'category_test';
    protect_object_id int := 0;
BEGIN

    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-12', 3, protect_object_id);
    INSERT INTO score_category VALUES(DEFAULT, tourn_name, 'category_1', 15);

    RETURN 0;
END $$;
SELECT category_test_setup();

-- Make a tournament for the purposes of testing permissions
CREATE OR REPLACE FUNCTION permission_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    tourn_name varchar := 'permission_test';
    tourn_id int := 0;
    protect_object_id int := 0;
    protected_object_action_id int := 0;
    protected_object_permission_id int := 0;
    username varchar := '';
BEGIN

    -- Create a superuser
    username = 'superman';
    INSERT INTO account VALUES (username, 'manofsteel@fortressofsolitude.com', TRUE);
    INSERT INTO account_security VALUES (username, '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');


    -- Create a tournament that will be restricted
    INSERT INTO protected_object VALUES (DEFAULT) RETURNING id INTO protect_object_id;
    INSERT INTO tournament VALUES (DEFAULT, tourn_name, '2095-07-12', DEFAULT, protect_object_id) RETURNING id INTO tourn_id;

    -- Create a user with access to modify
    username = 'lex_luthor';
    INSERT INTO account VALUES (username, 'lex_luthor@evil_hideout.com');
    INSERT INTO account_security VALUES (username, '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');

    -- Give them permission to enter a score for it
    SELECT id INTO protected_object_action_id FROM protected_object_action WHERE description = 'enter_score' LIMIT 1;
    INSERT INTO protected_object_permission VALUES (DEFAULT, protect_object_id, 
        (SELECT id FROM protected_object_action
            WHERE description = 'enter_score' LIMIT 1)
        ) RETURNING id INTO protected_object_permission_id;
    INSERT INTO account_protected_object_permission VALUES (username, protected_object_permission_id);

    -- Create a basic player
    INSERT INTO account VALUES ('permission_test_player', 'permission_test_player@darkness.com');
    INSERT INTO account_security VALUES ('permission_test_player', '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D');
    INSERT INTO registration VALUES('permission_test_player', tourn_id);
    INSERT INTO entry VALUES(default, 'permission_test_player', 'permission_test');

    RETURN 0;
END $$;
SELECT permission_test_setup();
