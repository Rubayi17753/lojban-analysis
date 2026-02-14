import numpy as np
import pandas as pd
from tqdm import tqdm

from src.classes.table import Table
from src.inserts import insert_shapes, insert_rafsi_pos

pos_dict = {'132': '134',
        '231': '234',
        '342': '345', '145': '345', '142': '345',
        }

def main(output_df):

    df = Table('defs_rafsi', keep_default_na=False).dff
    df = df.rename(columns={'rafsi' : 'cmavo_rafsi'})
    df = insert_shapes(df)
    df = insert_rafsi_pos(df)
    df['rafsi_pos'] = df['rafsi_pos'].apply(lambda x : pos_dict.get(x, x))

    df.to_csv(output_df, sep=',', index=False)

    