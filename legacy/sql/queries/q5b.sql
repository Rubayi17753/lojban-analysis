-- Process concordance

WITH lojban1999_aggregate2 AS (
    SELECT rafsi_or_cmavo, as_rafsi FROM lojban1999_aggregate
)

SELECT
    lujvo_1999_concordance.lujvo_parsed AS lujvo_parsed,
    lujvo_for_split AS rafsi,
    rafsi_defs.gismu,

    CASE
        WHEN LENGTH(rafsi_defs.gismu) < 5 THEN 'c'
        WHEN LENGTH(rafsi_defs.gismu) = 5 THEN 'g'
        ELSE '_'
    END AS gismu_or_cmavo,

    rafsi_defs.meaning,
    lujvo_component_meanings.component_meaning AS component_meaning,
    lujvo_component_meanings.assigned_meaning AS meaning_lujv1999,
    -- noralujv.meaning AS meaning_noralujv,

    CASE
        WHEN lujvo_sequence = 0 THEN 'ini'
        WHEN lujvo_sequence = lujvo_len - 1 THEN 'fin'
        ELSE 'med'
    END AS position,

    lujvo_sequence,
    lujvo_len

    /*
    lojban1999_aggregate.gismu_total_freq as gismu_freq,
    lojban1999_aggregate2.as_rafsi as rafsi_freq
    */

FROM lujvo_1999_concordance 
    LEFT JOIN rafsi_defs
        ON lujvo_1999_concordance.lujvo_for_split = rafsi_defs.rafsi
    LEFT JOIN lujvo_component_meanings
        ON lujvo_1999_concordance.lujvo = lujvo_component_meanings.lujvo
    /*
    LEFT JOIN noralujv
        ON lujvo_1999_concordance.lujvo = noralujv.lujvo
    */

    /*
    LEFT JOIN lujvo_freqs_1999
        ON lujvo_1999_concordance.lujvo = lujvo_freqs_1999.
    */

    /*
    LEFT JOIN lojban1999_aggregate
        ON lujvo_1999_concordance.gismu = lojban1999_aggregate.gismu
    LEFT JOIN lojban1999_aggregate2
        ON lujvo_1999_concordance.rafsi = lojban1999_aggregate2.rafsi_or_cmavo
    */
;
