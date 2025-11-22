-- Obtain a list of cmavo rafsi

WITH rafsi_defs_renamed AS (
	SELECT 
		rafsi,
		gismu AS gismu_or_cmavo,
		meaning
FROM 
	rafsi_defs
)

SELECT 
	rafsi_defs_renamed.rafsi, 
	rafsi_defs_renamed.gismu_or_cmavo,
	cmavo_defs.class AS bai,
	rafsi_defs_renamed.meaning 
FROM 
	rafsi_defs_renamed
		JOIN cmavo_defs ON rafsi_defs_renamed.gismu_or_cmavo = cmavo_defs.cmavo
WHERE LENGTH(gismu_or_cmavo) < 5
ORDER BY bai ASC, rafsi_defs_renamed.meaning ASC
;