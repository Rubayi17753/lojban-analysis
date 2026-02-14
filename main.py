import os
import pandas as pd
pd.options.mode.chained_assignment = None

import src.df_phonemic, src.df_rafsi_pos
import src.df1, src.df1_q2, src.df3b

def main():

    summary_fp = 'results/summary.csv'

    # src.df_phonemic.main()
    src.df_rafsi_pos.main('results/rafsi_pos_shape.csv')

    df_grand_table = src.df1.create_grand_table()
    df1_q2 = src.df1_q2.main(df_grand_table)
    src.df3b.main(df1_q2, summary_fp, override_file='copy')
    if os.path.exists(summary_fp):
        from src.df4_lujvo import main as df4_lujvo
        df4_lujvo()

if __name__ == '__main__':
    main()