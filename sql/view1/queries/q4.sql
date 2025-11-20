-- Obtain gismu COUNTs in aggregate for Gini formulation purposes

SELECT
    count_gismu,
    COUNT(count_gismu)
FROM
    (
    SELECT
        COUNT(gismu) AS count_gismu
    FROM lojban1999_aggregate
    GROUP BY gismu
    )
GROUP BY count_gismu
ORDER BY count_gismu
;