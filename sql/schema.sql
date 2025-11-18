CREATE TABLE IF NOT EXISTS gismu_defs (
	gismu TEXT,
	theme_code TEXT,
	meaning TEXT,
	def TEXT
);

CREATE TABLE IF NOT EXISTS gismu_themes (
	theme_code TEXT,
	theme TEXT
);

CREATE TABLE IF NOT EXISTS rafsi_defs (
	rafsi TEXT,
	gismu TEXT,
	meaning TEXT
);

CREATE TABLE IF NOT EXISTS rafsi_freqs (
	-- Provisional table, later to be generated from another
	rafsi_or_cmavo TEXT,
	gismu TEXT,
	as_rafsi_ini NUMERIC,
	as_rafsi_med NUMERIC,
	as_rafsi_fin NUMERIC,
	as_gismu NUMERIC,
	as_cmavo NUMERIC
);

CREATE TABLE IF NOT EXISTS cmavo_defs (
	cmavo TEXT,
	gismu TEXT,
	class TEXT,
	meaning TEXT,
	def TEXT
);

CREATE TABLE IF NOT EXISTS obliques (
	gismu TEXT,
	position INTEGER,
	oblique TEXT
);

CREATE TABLE IF NOT EXISTS pos_substitutions (
	old_pos TEXT,
	new_pos TEXT
);
