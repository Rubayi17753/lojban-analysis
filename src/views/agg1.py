import os
import sqlite3
import pandas as pd
import csv
from tabulate import tabulate
from src.word_shape import word_shape
from src.substring_positions import substring_positions

def agg1(run_schema=0, mode='pandas', 
        drop_views=1, create_views=1,):
    
    # Connect
    conn = sqlite3.connect('data/lojban1999.db')
    cur = conn.cursor()

    # Register SQL function backed by Python module
    conn.create_function('word_shape', narg=1, func=word_shape)
    conn.create_function('substring_positions', narg=3, func=substring_positions)

    if run_schema:
        with open('sql/schema.sql', 'r', encoding='utf-8') as f:
            cur.executescript(f.read())

    if drop_views:
        execute_sql('drop_views', conn, cur)

    if create_views:
        execute_sql('create_views', conn, cur)

    query(conn, cur, mode)
    conn.close()

def execute_sql(sql_filename, conn, cur):
    with open(f'sql/view1/{sql_filename}.sql', 'r', encoding='utf-8') as f:
        cur.executescript(f.read())
    conn.commit()

def query(conn, cur, mode='pandas'):

    query_paths = [entry.path for entry in os.scandir('sql/view1/queries') 
                if entry.is_file()]
    
    for query_path in query_paths:
      
        with open(query_path, 'r', encoding='utf-8') as f:
            
            if mode == 'rows':
                result = cur.executescript(f.read())
                for row in result:
                    print(row)

            elif mode == 'pandas':          
                df = pd.read_sql_query(f.read(), conn)
                print(df.info())
                print(df)

            elif mode == 'tabulate':
                result = cur.executescript(f.read())
                rows = cur.fetchall()
                headers = [desc[0] for desc in cur.description]
                print(tabulate(rows, headers, tablefmt="grid"))

            elif mode == 'csv':
                ...

    conn.commit()

    

