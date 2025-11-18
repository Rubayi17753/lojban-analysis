CREATE VIEW IF NOT EXISTS positional_percentages AS
SELECT
    rafsi_or_cmavo,
    word_shape(rafsi_or_cmavo) AS rafsi_or_cmavo_shape,
    gismu,
    word_shape(gismu) AS gismu_shape,
    substring_positions(rafsi_or_cmavo, gismu, 'string') AS gismu_pos,
    as_rafsi_ini,
    as_rafsi_med,
    as_rafsi_fin,
    as_rafsi_ini + as_rafsi_med + as_rafsi_fin AS as_rafsi,
    as_rafsi_ini / (as_rafsi_ini + as_rafsi_med + as_rafsi_fin) AS percentage_ini,
    as_rafsi_med / (as_rafsi_ini + as_rafsi_med + as_rafsi_fin) AS percentage_med,
    as_rafsi_fin / (as_rafsi_ini + as_rafsi_med + as_rafsi_fin) AS percentage_fin,
    as_gismu,
    as_cmavo
FROM rafsi_freqs
;

CREATE VIEW IF NOT EXISTS gismu_freqs AS
SELECT
    gismu,
    SUM(as_rafsi_ini)
    + SUM(as_rafsi_med)
    + SUM(as_rafsi_fin) AS gismu_freq
FROM rafsi_freqs
GROUP BY gismu
;

CREATE VIEW IF NOT EXISTS lojban1999_aggregate AS
SELECT * 
FROM positional_percentages
    JOIN gismu_freqs
    ON positional_percentages.gismu = gismu_freqs.gismu
;