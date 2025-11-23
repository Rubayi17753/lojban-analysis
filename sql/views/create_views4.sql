-- Requires concordance

CREATE VIEW IF NOT EXISTS lujvo_component_meanings AS

    WITH lujvo_1999_concordance_distinct AS (
        SELECT DISTINCT 
            lujvo,
            lujvo_parsed,
            lujvo_for_split,
            lujvo_sequence,
            lujvo_len
    FROM 
        lujvo_1999_concordance
    )

    SELECT
        lujvo,
        lujvo_parsed,
        GROUP_CONCAT(rafsi_defs.meaning,'-') AS component_meaning,
        lujvo_freqs_1999.canon_meaning AS assigned_meaning
    FROM lujvo_1999_concordance_distinct 
        LEFT JOIN rafsi_defs
            ON lujvo_1999_concordance_distinct.lujvo_for_split = rafsi_defs.rafsi
        LEFT JOIN lujvo_freqs_1999
            ON lujvo_1999_concordance_distinct.lujvo = lujvo_freqs_1999.actual
    GROUP BY lujvo
;