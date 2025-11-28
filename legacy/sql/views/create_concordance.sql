-- Concordance

WITH 

    lujvo_list AS (
    SELECT
        section_id,
        sign,
        -- in order of priority: use actual if meaning given, new replaces actual
        CASE
            WHEN canon_meaning != '' THEN actual
            WHEN new != '' THEN new
            ELSE actual
        END AS lujvo
    FROM
        lujvo_freqs_1999
),

    lujvo_list2 AS (
    SELECT
        section_id
        ,sign
        ,lujvo
        ,lujvo_parse_as_string(lujvo) AS lujvo_parsed
        ,lujvo_length(lujvo) AS lujvo_len
    FROM
        lujvo_list
)

SELECT
    lujvo
    ,lujvo_parsed
    ,lujvo_parsed AS lujvo_for_split
    ,integer_to_series(lujvo_len, '-') AS lujvo_sequence
    ,lujvo_len
FROM
    lujvo_list2
WHERE
    lujvo != ''
    AND section_id = 11 
    AND sign != '%'
;