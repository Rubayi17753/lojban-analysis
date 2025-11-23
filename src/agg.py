import os
import sqlite3
import pandas as pd
import csv
from tabulate import tabulate

# Connect
conn = sqlite3.connect('data/lojban1999.db')
cur = conn.cursor()

# Register SQL function backed by Python module
def register_functions():

    from src.lojban_specific.word_shape import word_shape
    from src.query_aux.parser_aux import lujvo_parse_as_string, lujvo_length
    from src.substring_positions import substring_positions
    from sql.query_aux.q5 import integer_to_series

    conn.create_function('word_shape', narg=1, func=word_shape)
    conn.create_function('substring_positions', narg=4, func=substring_positions)
    conn.create_function('lujvo_parse_as_string', narg=1, func=lujvo_parse_as_string)
    conn.create_function('lujvo_length', narg=1, func=lujvo_length)
    conn.create_function('integer_to_series', narg=2, func=integer_to_series)

def agg(view_num, run_schema=0, mode='pandas', 
        drop_views=1, create_views=1, run_queries=1, close=1,):

    register_functions()

    if run_schema:
        with open('sql/schema.sql', 'r', encoding='utf-8') as f:
            cur.executescript(f.read())

    if drop_views:
        execute_sql('drop_views', conn, cur)

    if create_views:
        execute_sql(f'create_views{view_num}', conn, cur)

    if run_queries:
        query(conn, cur, mode)

    if close:
        conn.close()

def agg_concordance(run_schema=0, mode='pandas', 
        drop_views=1, create_views=1,):

    from sql.query_aux.q5 import main as q5

    register_functions()
    
    if create_views:
        execute_sql('create_concordance', conn, cur)    
    query(conn, cur, mode)
    q5()

    conn.close()

def execute_sql(sql_filename, conn, cur):
    with open(f'sql/views/{sql_filename}.sql', 'r', encoding='utf-8') as f:
        cur.executescript(f.read())
    conn.commit()

def query(conn, cur, mode='pandas'):

    query_paths = [entry.path 
                for entry in os.scandir('sql/queries') 
                if entry.is_file()]
    filenames = [os.path.splitext(os.path.basename(query_path))[0]
                for query_path in query_paths]
    query_paths_filenames = [(query_path, filename)
                for query_path, filename
                in zip(query_paths, filenames)
                if not filename.startswith('u_')]

    for query_path, filename in query_paths_filenames:
      
        with open(query_path, 'r', encoding='utf-8') as f:

            # Check if module sql.queries.[query_path] exists
            # Import as [query_path]
            # Run [query_path]()

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

    

