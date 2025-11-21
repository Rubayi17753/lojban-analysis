import pandas as pd
import sqlite3

def csv_to_table(csv_path, table_name, table_path):

    df = pd.read_csv(csv_path, skiprows=1)  # skiprows skips the header
    conn = sqlite3.connect(table_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False, 
                index_label='rowid')