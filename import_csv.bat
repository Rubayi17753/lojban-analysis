sqlite3 data/lojban1999.db < sql/schema.sql
for %%f in (data\lojban1999\*.csv) do (
    sqlite3 data\lojban1999.db ".import --csv --skip 1 %%f %%~nf"
)
pause