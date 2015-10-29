INSERT INTO tournament VALUES (DEFAULT, 'northcon_2095');
INSERT INTO tournament VALUES (DEFAULT, 'southcon_2095');
INSERT INTO tournament VALUES (DEFAULT, 'conquest_2095');

DO $$
DECLARE lastid int := 0;
BEGIN
    INSERT INTO account VALUES (DEFAULT, 'foo@bar.com') RETURNING id INTO lastid;
    INSERT INTO player VALUES (lastid, 'stevemcqueen', NULL);
END $$;
