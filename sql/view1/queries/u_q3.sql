-- 'official' rafsi that are not in the frequency table

SELECT rafsi, gismu
FROM rafsi_defs
WHERE 
    (rafsi, gismu) NOT IN (SELECT rafsi_or_cmavo, gismu FROM rafsi_freqs)
    AND LENGTH(gismu) = 5
;
