-- Set up some tournaments
INSERT INTO tournament VALUES (DEFAULT, 'northcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'southcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'conquest_2095', '2095-10-31');
INSERT INTO tournament VALUES (DEFAULT, 'painting_test', '2095-10-10');

INSERT INTO score_key VALUES (DEFAULT, 'fanciest_wig', 'painting_test', 4, 15);
INSERT INTO score_key VALUES (DEFAULT, 'number_tassles', 'painting_test', 2, 28);


-- Set up some users
DO $$
DECLARE lastid int := 0;
BEGIN
    INSERT INTO account VALUES (DEFAULT, 'foo@bar.com') RETURNING id INTO lastid;
    INSERT INTO player VALUES (lastid, 'stevemcqueen', NULL);
    INSERT INTO account_security VALUES (lastid, '$5$rounds=535000$gEkrAmEJxdn30HMR$HPPOeXufYDksVGLSUbj5TqJVKKRTBsU31VsetE9oeI0');
    INSERT INTO account VALUES (DEFAULT, 'foo@bar.com') RETURNING id INTO lastid;
    INSERT INTO player VALUES (lastid, 'rick_james', NULL);
    INSERT INTO account_security VALUES (lastid, '$5$rounds=535000$gEkrAmEJxdn30HMR$HPPOeXufYDksVGLSUbj5TqJVKKRTBsU31VsetE9oeI0');
    INSERT INTO account VALUES (DEFAULT, 'chalie_murphy@darkness.com') RETURNING id INTO lastid;
    INSERT INTO player VALUES (lastid, 'charlie_murphy', NULL);
    INSERT INTO account_security VALUES (lastid, '$5$rounds=535000$1ChlmvAIh/6yDqVg$wn8vZxK1igRA17V8pjMr90ph3Titr35DF5X5DYSLpv.');
END $$;


-- Enter some players
INSERT INTO registration VALUES('stevemcqueen', 'painting_test');

INSERT INTO entry VALUES(default, 'rick_james', 'painting_test');


-- Make a tournament for the purposes of testing rankings
CREATE OR REPLACE FUNCTION ranking_test_setup() RETURNS int LANGUAGE plpgsql AS $$
DECLARE
    accid int := 0;
    eid int := 0;
    rd1key int := 0;
    rd2key int := 0;
    sportskey int := 0;
BEGIN

    INSERT INTO tournament VALUES (DEFAULT, 'ranking_test', '2095-08-12');


    INSERT INTO score_key VALUES (DEFAULT, 'round_1_battle', 'ranking_test', 0, 20) RETURNING id INTO rd1key;
    INSERT INTO score_key VALUES (DEFAULT, 'round_2_battle', 'ranking_test', 0, 20) RETURNING id INTO rd2key;
    INSERT INTO score_key VALUES (DEFAULT, 'sports', 'ranking_test', 1, 5) RETURNING id INTO sportskey;


    INSERT INTO account VALUES (DEFAULT, 'foo@bar.com') RETURNING id INTO accid;
    INSERT INTO player VALUES (accid, 'homer', NULL);
    INSERT INTO account_security VALUES (accid, '$5$rounds=535000$gEkrAmEJxdn30HMR$HPPOeXufYDksVGLSUbj5TqJVKKRTBsU31VsetE9oeI0');
    INSERT INTO registration VALUES('homer', 'ranking_test');
    INSERT INTO entry VALUES(default, 'homer', 'ranking_test') RETURNING id INTO eid;
    INSERT INTO score VALUES(eid, rd1key, 20);
    INSERT INTO score VALUES(eid, rd2key, 15);
    INSERT INTO score VALUES(eid, sportskey, 1);


    INSERT INTO account VALUES (DEFAULT, 'foo@bar.com') RETURNING id INTO accid;
    INSERT INTO player VALUES (accid, 'marge', NULL);
    INSERT INTO account_security VALUES (accid, '$5$rounds=535000$gEkrAmEJxdn30HMR$HPPOeXufYDksVGLSUbj5TqJVKKRTBsU31VsetE9oeI0');
    INSERT INTO registration VALUES('marge', 'ranking_test');
    INSERT INTO entry VALUES(default, 'marge', 'ranking_test') RETURNING id INTO eid;
    INSERT INTO score VALUES(eid, rd1key, 0);
    INSERT INTO score VALUES(eid, rd2key, 5);
    INSERT INTO score VALUES(eid, sportskey, 5);

    RETURN 0;
END $$;
SELECT ranking_test_setup()
