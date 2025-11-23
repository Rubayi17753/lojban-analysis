Raw tables:
- cmavo_defs
- gismu_defs
- gismu_themes
- obliques
- rafsi_defs
- rafsi_freqs:
    - rafsi_or_cmavo
    - gismu
    - as_rafsi_ini
    - as_rafsi_mid
    - as_rafsi_fin
    - as_gismu
    - as_cmavo

Stage 2:
Intermediate tables
- pos_substitutions <-- q2

Stage 3:
- (new) rafsi_freqs <-- lujvo_freqs_1999_freqs

Stage 4:
- ... --> q5_concordances_unpacked.csv --> lujvo_1999_concordance (intermediate table)
- lujvo_1999_concordance + lujvo_freqs_1999 (secondary) --view4--> lujvo_component_meanings
- lujvo_component_meanings --> q5b

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


