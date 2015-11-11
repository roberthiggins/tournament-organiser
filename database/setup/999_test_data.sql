INSERT INTO tournament VALUES (DEFAULT, 'northcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'southcon_2095', '2095-06-01');
INSERT INTO tournament VALUES (DEFAULT, 'conquest_2095', '2095-10-31');
INSERT INTO tournament VALUES (DEFAULT, 'painting_test', '2095-10-10');

DO $$
DECLARE lastid int := 0;
BEGIN
    INSERT INTO account VALUES (DEFAULT, 'foo@bar.com') RETURNING id INTO lastid;
    INSERT INTO player VALUES (lastid, 'stevemcqueen', NULL);
END $$;

INSERT INTO registration VALUES('stevemcqueen', 'painting_test');
