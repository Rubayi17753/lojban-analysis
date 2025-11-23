-- Process concordance

SELECT
    lujvo_1999_concordance.lujvo_parsed AS lujvo_parsed,
    lujvo_for_split AS rafsi,
    rafsi_defs.gismu,
    rafsi_defs.meaning,
    lujvo_component_meanings.component_meaning AS component_meaning,
    lujvo_component_meanings.assigned_meaning AS meaning_lujv1999,
    noralujv.meaning AS meaning_noralujv
    CASE
        WHEN lujvo_sequence = 0 THEN 'ini'
        WHEN lujvo_sequence = lujvo_len - 1 THEN 'fin'
        ELSE 'med'
    END AS position,
    lujvo_sequence,
    lujvo_len
FROM lujvo_1999_concordance 
    JOIN rafsi_defs
        ON lujvo_1999_concordance.lujvo_for_split = rafsi_defs.rafsi
    JOIN lujvo_component_meanings
        ON lujvo_1999_concordance.lujvo = lujvo_component_meanings.lujvo
    JOIN noralujv
        ON lujvo_1999_concordance.lujvo = noralujv.lujvo
    /*
    LEFT JOIN lujvo_freqs_1999
        ON lujvo_1999_concordance.lujvo = lujvo_freqs_1999.
    */
;
