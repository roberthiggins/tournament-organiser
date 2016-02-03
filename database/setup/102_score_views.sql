CREATE VIEW player_score AS
    SELECT
        e.player_id             AS username,
        c.display_name          AS category,
        k.key,
        s.value                 AS score,
        k.min_val,
        k.max_val,
        c.percentage,
        r.round_id              AS for_round,
        c.tournament_id         AS tournament,
        e.id                    AS entry_id,
        c.id                    AS category_id
    FROM score                  s
    INNER JOIN score_key        k ON s.score_key_id = k.id
    INNER JOIN score_category   c ON k.category = c.id
    INNER JOIN entry            e ON s.entry_id = e.id
    INNER JOIN round_score      r ON k.id = r.score_key_id
    ORDER BY tournament ASC, username ASC, for_round ASC
;
