-- Deals with lujvo1999_freqs


CREATE VIEW IF NOT EXISTS form_types2 AS
SELECT
    *
    /*
    form_types.rafsi_or_cmavo,
    form_types.gismu,
    pos_substitutions.new_pos AS rafsi_or_cmavo_pos,     -- misnomer fixed
    form_types.form_type
    */
FROM lujvo1999
    LEFT JOIN pos_substitutions
        ON form_types.gismu_pos = pos_substitutions.old_pos
;

CREATE VIEW IF NOT EXISTS lojban1999_aggregate AS
SELECT * 
FROM positional_percentages
    JOIN gismu_freqs
        ON positional_percentages.gismu = gismu_freqs.gismu
    JOIN form_freqs2
        ON positional_percentages.rafsi_or_cmavo = form_freqs2.rafsi_or_cmavo
        AND positional_percentages.gismu = form_freqs2.gismu
    JOIN form_types2
        ON positional_percentages.rafsi_or_cmavo = form_types2.rafsi_or_cmavo
        AND positional_percentages.gismu = form_types2.gismu
    JOIN gismu_defs
        ON positional_percentages.gismu = gismu_defs.gismu
;