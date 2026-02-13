import os
import pandas as pd
from src.df_phonemic import main as df_gismu_phonemic
from src.df3b import main as df3b

def main():

    summary_fp = 'results/summary.csv'

    pd.options.mode.chained_assignment = None
    df_gismu_phonemic()
    df3b(summary_fp, override_file='copy')
    if os.path.exists(summary_fp):
        from src.df4_lujvo import main as df4_lujvo
        df4_lujvo()

if __name__ == '__main__':
    main()