sqlite3 data/lojban1999.db < sql/schema.sql
sqlite3 data\lojban1999.db ".import --csv --skip 1 data/intermediate/q5_concordances_unpacked.csv lujvo_1999_concordance"
pause