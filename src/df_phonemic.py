from src.classes.table import Table
from src.lojban_specific.parser import syllable_parser

def main():

    df = Table('defs_gismu').dff[['gismu']]
    df['gismu_parsed'] = df['gismu'].apply(lambda x: syllable_parser(x, delim='-'))
    df.to_csv('results/df_phonemic_gismu.tsv', sep='\t', index=False)

    df = Table('defs_rafsi', keep_default_na=False).dff[['rafsi']]
    df['rafsi_parsed'] = df['rafsi'].apply(lambda x: syllable_parser(x, delim='-'))
    df.to_csv('results/df_phonemic_rafsi.tsv', sep='\t', index=False)