import pandas as pd
from src.df_phonemic import main as df_gismu_phonemic
from src.df3b import main as df3b
from src.df4_lujvo import main as df4_lujvo

def main():
    pd.options.mode.chained_assignment = None
    df_gismu_phonemic()
    df3b(override_file='copy')
    df4_lujvo()

if __name__ == '__main__':
    main()