INSERT INTO tournament VALUES (DEFAULT, 'northcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'southcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'conquest_2095', '2095-10-31');
INSERT INTO tournament VALUES (DEFAULT, 'painting_test', '2095-10-10');

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

INSERT INTO registration VALUES('stevemcqueen', 'painting_test');
