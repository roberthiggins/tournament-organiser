/*
A score_category is essentially a way to classify scores that might have to be
modified from their raw values. e.g. A battle score might be worth 60% of the
tournament points; A painting score might be ignored for determing matchups; etc.
*/

CREATE TABLE score_category(
    id                  SERIAL PRIMARY KEY,
    tournament_id       VARCHAR NOT NULL REFERENCES tournament(name),
    display_name        VARCHAR UNIQUE NOT NULL,
    percentage          INTEGER NOT NULL DEFAULT 100
);
COMMENT ON COLUMN score_category.percentage IS 'The raw score should be multiplied by this.';
