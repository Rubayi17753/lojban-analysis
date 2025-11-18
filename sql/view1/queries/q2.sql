-- Obtain 'inventory' of types of gismu > rafsi derivations

SELECT 
    rafsi_or_cmavo_len, rafsi_or_cmavo_shape, gismu_shape, gismu_pos,
    COUNT(*) 
FROM lojban1999_aggregate
GROUP BY rafsi_or_cmavo_len, rafsi_or_cmavo_shape, gismu_shape, gismu_pos
ORDER BY COUNT(*) DESC
;