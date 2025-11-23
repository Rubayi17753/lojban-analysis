-- Requires concordance
CREATE VIEW IF NOT EXISTS lujvo_component_meanings AS

    WITH 
        lujvo_1999_concordance_distinct AS (
            SELECT DISTINCT 
                lujvo,
                lujvo_parsed,
                lujvo_for_split,
                lujvo_sequence,
                lujvo_len
        FROM 
            lujvo_1999_concordance
        ),

        meanings AS (
        SELECT 
            rafsi AS form, meaning FROM rafsi_defs
            UNION SELECT gismu AS form, meaning FROM rafsi_defs     
            UNION SELECT substring(gismu, 1, LENGTH(gismu)) AS form, meaning FROM rafsi_defs     
        )

    SELECT
        lujvo,
        lujvo_parsed,
        GROUP_CONCAT(meanings.meaning,'-') AS component_meaning,
        lujvo_freqs_1999.canon_meaning AS assigned_meaning
    FROM lujvo_1999_concordance_distinct 
        LEFT JOIN meanings
            ON lujvo_1999_concordance_distinct.lujvo_for_split = meanings.form
        LEFT JOIN lujvo_freqs_1999
            ON lujvo_1999_concordance_distinct.lujvo = lujvo_freqs_1999.actual
    GROUP BY lujvo
;