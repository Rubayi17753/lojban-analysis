# tl;dr (arrows indicate dependence)

data/lojban1999 --> df1
data/lojban1999 --> df2
df2(a) --> df1
df1 --> df1_q1
df1 --> df1_q2
df1_q1 --> df3
df1_q2 --> df3

# A longer description

The pandas-based 'queries' in src (designated by initial df) relate as follows:

df1 generates frequencies of forms in various forms and frequencies.
    as_gismu,
    as_rafsi_conv,
    as_rafsi_i,
    as_rafsi_m,
    as_rafsi_f,
    as_cmavo,
    as_cmavo_compound
The `as_rafsi` frequencies are taken from df2a.

df2 generates two results:
    - df2a : database of rafsi positional frequencies `rafsi,conversion,fin,ini,med,gismu`
    - df2b : concordance (list of lujvo that contains rafsi in a certain position)
df2 does not depend on df1. df2a is fed back to df1 to produce a more 'general' frequency database.
Note : df2 has, by default, several of my custom 'filters' applied. To obtain 'canonical' Lojban data, disable them by passing `parameter=0` or `parameter=False` to the module's `main()`.

df1 is then queried to produce two results:
    - df1_q1 : merges rafsi frequencies --> gismu frequencies
    - df1_q2 : df1 (rafsi data) elaborated

## Hic incipit corpus separatum

df3 feeds on df1_q1 and df1_q2. It contains:
    - a list of gismu
    - forms (rafsi + cmavo) associated with each gismu that passes through a series of filters, ordered by frequency
    - forms that don't