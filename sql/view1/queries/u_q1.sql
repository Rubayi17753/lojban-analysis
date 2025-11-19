SELECT

    rafsi_or_cmavo,
    rafsi_or_cmavo_shape,
    form_type,
    gismu,
    gismu_shape,
    new_pos AS rafsi_or_cmavo_pos,
    gismu_total_freq,
    percentage_form,
    percentage_ini,
    percentage_med,
    percentage_fin,

    as_rafsi_ini,
    as_rafsi_med,
    as_rafsi_fin,

    as_rafsi,
    as_cmavo,
    as_gismu,
    form_total_freq,
    gismu_total_freq

FROM lojban1999_aggregate

ORDER BY
    percentage_form DESC,
    rafsi_or_cmavo_shape ASC,
    rafsi_or_cmavo_pos ASC,
    gismu_total_freq DESC

-- WHERE theme_code NOT IN ('12.3', '12.4', '12.5.1') -- excludes religio-cultural-gismu
;