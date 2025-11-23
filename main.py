from src.agg import agg, agg_concordance
from src.csv_to_table import csv_to_table


def main():

    csv_path = 'data/lojban1999/lujvo_freqs_1999_freqs.csv'
    table_path = 'data/lojban1999.db'
    table_name = 'lujvo_freqs_1999'

    # csv_to_table(csv_path, table_path, table_name)

    # Run the following one at a time:
    # agg(view_num=1, run_schema=0, run_queries=0, mode='tsv',)
    # agg(view_num=2, run_schema=0, run_queries=0, mode='tsv',)
    agg(view_num=4, run_schema=0,  mode='tsv',)

if __name__ == '__main__':
    main()