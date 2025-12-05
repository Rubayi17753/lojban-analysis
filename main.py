import pandas as pd
from src.df3b import main as df3b

def main():
    pd.options.mode.chained_assignment = None
    df3b(override_file='update')

if __name__ == '__main__':
    main()