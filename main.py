from src.agg import agg1, agg2, agg3
from src.csv_to_table import csv_to_table

def main():

    csv_path = 'data/lojban1999/lujvo_freqs_1999_freqs.csv'
    table_path = 'data/lojban1999.db'
    table_name = 'lujvo_freqs_1999'

    # csv_to_table(csv_path, table_path, table_name)
    agg2(run_schema=1, mode='tsv',) 

if __name__ == '__main__':
    main()