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
	as_rafsi_ini NUMERIC NOT NULL DEFAULT 0,
	as_rafsi_med NUMERIC NOT NULL DEFAULT 0,
	as_rafsi_fin NUMERIC NOT NULL DEFAULT 0,
	as_gismu NUMERIC NOT NULL DEFAULT 0,
	as_cmavo NUMERIC NOT NULL DEFAULT 0
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

CREATE TABLE IF NOT EXISTS lujvo_freqs_1999 (
	section_id INTEGER,	-- corresponds to notes/lujvo_freqs_1999notes.md
	freq_raw TEXT,	-- to be converted to actual frequencies through a function/algorithm
	sign TEXT,
	actual TEXT,
	actual_breakdown TEXT,
	canon TEXT,
	canon_breakdown TEXT,
	canon_meaning TEXT,
	canon_places TEXT,
	new TEXT,
	new_breakdown TEXT
);

-- Created after running views.create_concordance (formerly q5)
CREATE TABLE IF NOT EXISTS lujvo_1999_concordance (
	rowid INTEGER,
	lujvo TEXT,
	lujvo_parsed TEXT,
	lujvo_for_split TEXT,
	lujvo_sequence INTEGER,
	lujvo_len INTEGER,
	PRIMARY KEY (rowid)
);

CREATE TABLE IF NOT EXISTS noralujv (
	lujvo TEXT,
	meaning TEXT
);
