CREATE VIEW IF NOT EXISTS positional_percentages AS
SELECT
    rafsi_or_cmavo,
    word_shape(rafsi_or_cmavo) AS rafsi_or_cmavo_shape,
    LENGTH(REPLACE(rafsi_or_cmavo, "'", '')) AS rafsi_or_cmavo_len,
    gismu,
    word_shape(gismu) AS gismu_shape,
    as_rafsi_ini,
    as_rafsi_med,
    as_rafsi_fin,
    as_rafsi_ini + as_rafsi_med + as_rafsi_fin AS as_rafsi, 
    as_gismu,

    CASE 
        WHEN as_cmavo = '' THEN 0
        ELSE as_cmavo END 
    AS as_cmavo
FROM rafsi_freqs
;

-- This view created after analysis of q2 
-- ('inventory' of types of gismu > rafsi derivation)
-- CREATE VIEW IF NOT EXISTS gismu_new_positions
-- ...
-- FROM positional_percentages

CREATE VIEW IF NOT EXISTS gismu_freqs AS
SELECT
    gismu,
    ROUND(
        SUM(as_rafsi)
        + SUM(as_gismu)
        + SUM(as_cmavo)
    ) AS gismu_total_freq,

    ROUND(as_rafsi_ini * 1.000 / (as_rafsi * 1.000) * 100, 1) AS percentage_ini,
    ROUND(as_rafsi_med * 1.000 / (as_rafsi * 1.000) * 100, 1) AS percentage_med,
    ROUND(as_rafsi_fin * 1.000 / (as_rafsi * 1.000) * 100, 1) AS percentage_fin
FROM positional_percentages
GROUP BY gismu
;

CREATE VIEW IF NOT EXISTS form_freqs AS
SELECT 
    positional_percentages.rafsi_or_cmavo,
    positional_percentages.gismu,
    as_rafsi + as_gismu + as_cmavo AS form_total_freq,
    gismu_freqs.gismu_total_freq
FROM positional_percentages
    JOIN gismu_freqs
        ON positional_percentages.gismu = gismu_freqs.gismu
;

CREATE VIEW IF NOT EXISTS form_freqs2 AS
SELECT 
    rafsi_or_cmavo,
    gismu,
    form_total_freq,
    ROUND(form_total_freq * 1.0 / (gismu_total_freq * 1.0) * 100, 1) AS percentage_form
FROM form_freqs
;

CREATE VIEW IF NOT EXISTS form_types AS
SELECT
    rafsi_or_cmavo,
    gismu,

    CASE
        WHEN rafsi_or_cmavo_len = 3 
            THEN substring_positions(gismu, REPLACE(rafsi_or_cmavo, "'", ''), 'string', ' ') 
        ELSE '' END 
    AS gismu_pos,   -- identified misnomer

    CASE
        WHEN 
            (rafsi_or_cmavo, gismu) IN (SELECT rafsi, gismu FROM rafsi_defs) 
            AND rafsi_or_cmavo IN (SELECT cmavo FROM cmavo_defs)
            THEN 'rafsi/cmavo'
        WHEN 
            (rafsi_or_cmavo, gismu) IN (SELECT rafsi, gismu FROM rafsi_defs) 
            THEN 'rafsi'
        WHEN
            rafsi_or_cmavo IN (SELECT cmavo FROM cmavo_defs)
            THEN 'cmavo'
        /*
        WHEN
            rafsi_or_cmavo_len IN (4, 5)
            THEN 'rafsi5'
        */
        ELSE '?' END 
    AS form_type
FROM positional_percentages
;

CREATE VIEW IF NOT EXISTS lojban1999_aggregate AS
SELECT * 
FROM positional_percentages
    JOIN gismu_freqs
        ON positional_percentages.gismu = gismu_freqs.gismu
    JOIN form_freqs2
        ON positional_percentages.rafsi_or_cmavo = form_freqs2.rafsi_or_cmavo
        AND positional_percentages.gismu = form_freqs2.gismu
    JOIN form_types
        ON positional_percentages.rafsi_or_cmavo = form_types.rafsi_or_cmavo
        AND positional_percentages.gismu = form_types.gismu
    JOIN gismu_defs
        ON positional_percentages.gismu = gismu_defs.gismu
;