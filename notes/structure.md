Raw tables:
- cmavo_defs
- gismu_defs
- gismu_themes
- obliques
- rafsi_defs
- rafsi_freqs

Intermediate tables
- pos_substitutions <-- q2

Views:
- positional_percentages <-- rafsi_freqs
- gismu_freqs <-- positional_percentages
- form_freqs <-- positional_percentages + gismu_freqs
- form_freqs2 <-- form_freqs
- form_types <-- positional_percentages
- lojban1999_aggregate <-- gismu_freqs + form_freqs2 + form_types + gismu_defs

Queries:
- q1 <-- lojban1999_aggregate (*)
- q2 <-- lojban1999_aggregate (rafsi_or_cmavo_len, rafsi_or_cmavo_shape, gismu_shape, gismu_pos,)


