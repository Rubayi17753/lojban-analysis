import os
import sqlite3
import pandas as pd
import csv
from tabulate import tabulate
from src.lojban_specific.word_shape import word_shape
from src.lojban_specific.parser import lujvo_parse_as_string
from src.substring_positions import substring_positions

# Connect
conn = sqlite3.connect('data/lojban1999.db')
cur = conn.cursor()

# Register SQL function backed by Python module
def register_functions():
    conn.create_function('word_shape', narg=1, func=word_shape)
    conn.create_function('substring_positions', narg=4, func=substring_positions)
    conn.create_function('lujvo_parse_as_string', narg=4, func=lujvo_parse_as_string)

def agg1(run_schema=0, mode='pandas', 
        drop_views=1, create_views=1,):

    register_functions()

    if run_schema:
        with open('sql/schema.sql', 'r', encoding='utf-8') as f:
            cur.executescript(f.read())

    if drop_views:
        execute_sql('drop_views', conn, cur)

    if create_views:
        execute_sql('create_views', conn, cur)

    query(conn, cur, mode)
    conn.close()

def agg2(run_schema=0, mode='pandas', 
        drop_views=1, create_views=1,):

    register_functions()
    
    if create_views:
        execute_sql('create_views2', conn, cur)    

    query(conn, cur, mode)
    conn.close()

def agg3(run_schema=0, mode='pandas', 
        drop_views=1, create_views=1,):

    register_functions()
    
    if create_views:
        execute_sql('create_views3', conn, cur)    

    query(conn, cur, mode)
    conn.close()

def execute_sql(sql_filename, conn, cur):
    with open(f'sql/view1/{sql_filename}.sql', 'r', encoding='utf-8') as f:
        cur.executescript(f.read())
    conn.commit()

def query(conn, cur, mode='pandas'):

    query_paths = [entry.path 
                for entry in os.scandir('sql/view1/queries') 
                if entry.is_file()]
    filenames = [os.path.splitext(os.path.basename(query_path))[0]
                for query_path in query_paths]
    query_paths_filenames = [(query_path, filename)
                for query_path, filename
                in zip(query_paths, filenames)
                if not filename.startswith('u_')]

    for query_path, filename in query_paths_filenames:
      
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

            elif mode == 'tsv':
                df = pd.read_sql_query(f.read(), conn)
                df.to_csv(f'results/{filename}_result.tsv', sep='\t', index=False)
                print(f'Results written to {filename}_result.tsv')

    conn.commit()

    

