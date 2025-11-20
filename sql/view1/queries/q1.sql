SELECT

    rafsi_or_cmavo,
    rafsi_or_cmavo_shape,
    form_type,
    gismu,
    gismu_shape,
    new_pos AS rafsi_or_cmavo_pos, -- requires agg2
    
    as_rafsi,
    as_cmavo,
    as_gismu,
    form_total_freq,
    gismu_total_freq,

    percentage_form,

    percentage_ini,
    percentage_med,
    percentage_fin,
    ROUND(((ABS(percentage_ini - percentage_med) + ABS(percentage_med - percentage_fin) + ABS(percentage_fin - percentage_ini)) / 2), 1)
        AS gini_pos

    /*
    as_rafsi_ini,
    as_rafsi_med,
    as_rafsi_fin,
    */

FROM lojban1999_aggregate

WHERE theme_code NOT IN (
    '12.3', '12.4', '12.5.1' -- excludes religio-cultural-gismu
    )
    AND gismu NOT LIKE 'brod_'

ORDER BY
    percentage_form DESC,
    gismu ASC,
    rafsi_or_cmavo_shape ASC,
    rafsi_or_cmavo_pos ASC,  -- requires agg2
    gismu_total_freq DESC
;