import pandas as pd
from src.classes.table import Table

def _fetch_data():
    df = Table('defs_cmavo', keep_default_na=False).dff
    df2 = Table('defs_rafsi', keep_default_na=False).dff
    df = df.merge(df2, how='right', left_on='cmavo', right_on='gismu')

def rafsi_list(selmao):
    df = _fetch_data()
    return df[df['class'] == selmao]['rafsi'].to_list()
    