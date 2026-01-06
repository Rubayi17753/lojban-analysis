import pandas as pd
from src.classes.table import Table

def main():
    df = Table('defs_cmavo', keep_default_na=False).dff

    df1 = df[df['class'] == 'BAI']
    print(df1)
    exit()