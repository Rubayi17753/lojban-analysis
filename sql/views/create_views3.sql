-- Deals with lujvo1999_freqs

WITH lujvo_freqs AS (
    SELECT
        -- in order of priority: use actual if meaning given, new replaces actual
        CASE
            WHEN canon_meaning != '' THEN actual
            WHEN new != '' THEN new
            ELSE actual
        END AS lujvo,
        somedamnedfunction(freq_raw) AS freq
    FROM
        lujvo1999
)

SELECT 
    lujvo_parse_as_string(lujvo),
    freq
FROM
    lujvo_freqs
WHERE
    section_id = 11
;