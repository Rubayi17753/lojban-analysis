from src.agg import agg, agg_concordance
from src.csv_to_table import csv_to_table


def main():

    csv_path = 'data/lojban1999/lujvo_freqs_1999_freqs.csv'
    table_path = 'data/lojban1999.db'
    table_name = 'lujvo_freqs_1999'

    # csv_to_table(csv_path, table_path, table_name)
    agg(view_num=4, run_schema=0, mode='tsv',)

if __name__ == '__main__':
    main()