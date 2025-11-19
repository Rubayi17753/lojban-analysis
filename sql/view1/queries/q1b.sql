SELECT
    rafsi_or_cmavo,
    gismu,
    percentage_form,
    gismu_total_freq

FROM lojban1999_aggregate

ORDER BY
    percentage_form DESC

-- WHERE theme_code NOT IN ('12.3', '12.4', '12.5.1') -- excludes religio-cultural-gismu
;