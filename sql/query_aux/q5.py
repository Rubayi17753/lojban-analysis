from src.uncouple_csv import uncouple_csv

def main():

    csv_in = 'results/q5_result.tsv'
    fp_out = 'results/q5_results_unpacked.csv'
    cols = ['lujvo_for_split', 'lujvo_sequence']
    out = uncouple_csv(csv_in, cols, fp_out, delim='-')

def integer_to_series(n, delim=''):
    # Example: 5 -> 01234
    return delim.join((str(i) for i in range(n)))