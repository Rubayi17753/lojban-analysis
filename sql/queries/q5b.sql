SELECT
    lujvo_for_split AS rafsi,
    rafsi_defs.gismu,
    lujvo_parsed,
    CASE
        WHEN lujvo_sequence = 0 THEN 'ini'
        WHEN lujvo_sequence = lujvo_len - 1 THEN 'fin'
        ELSE 'med'
    END AS position,
    lujvo_sequence,
    lujvo_len
FROM lujvo_1999_concordance JOIN rafsi_defs
    ON lujvo_1999_concordance.lujvo_for_split = rafsi_defs.rafsi

;
