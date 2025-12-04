import numpy as np
import pandas as pd
from tqdm import tqdm
import src.inserts as inserts
from src.df1_q1 import main as dfq1
from src.df1_q2 import main as dfq2
from src.tools.class_table import Table
from src.df3_shared import determine_pos_tendency
from src.lojban_specific.word_shape import word_shape

def get_frequency_order(df):
    df['frequency_order'] = df.groupby('gismu')['gismu'].cumcount() + 1
    return df

def mask1(df):

    excludeds = ("a'a", "e'e", "i'i", "o'o", "u'u",
                "ei", "e'i", "o'u")
    mask = (
        (df['coef1'] > 2) &   # Coefficient here: q2's df['cmavo_rafsi_freq'] / df['max_form_freq'] * 100
        (~df['rafsi_pos'].str.contains('_'))
        # (~df['cmavo_rafsi'].str.slice(start=1).isin(excludeds))
    )
    return mask

def mask2(df):
    return (df['cmavo_rafsi'].str.len() != 5)

def aggregate(df):

    mask = mask1(df)
    df2 = df.copy()
    df2['form_len'] = df2['rafsi_pos'].str.len()
    df2 = df2.sort_values(by=['form_len', 'rafsi_pos'])

    df = df.assign(
                excluded=df['cmavo_rafsi'].where(~mask, ''),
            ).groupby('gismu', as_index=False).agg(
                excluded=('excluded', ' '.join),
    )

    df2 = df2.assign(
                rafsi_pos=df2['rafsi_pos'].where(mask, ''),
            ).groupby('gismu', as_index=False).agg(
                rafsi_pos=('rafsi_pos', ' '.join),
    )

    df2['rafsi_pos'] = df2['rafsi_pos'].str.strip()
    df = pd.concat([df, df2['rafsi_pos']], axis=1)
    return df

def determine_pos_tendency(df):
    # Determine rafsi positioning tendency
    # Requires dfq1() --> coef2
    cols = ['as_rafsi', 'percentage_im', 'percentage_fm', 'coef2']

    # Sanitisation
    for col in cols:
        df[col] = (pd.to_numeric(df[col], errors='coerce')
        .replace(np.inf, 999)
        .replace(-np.inf, -999)
        )

    df[cols] = df[cols].fillna(0)

    conditions = [
        (df['as_rafsi'] == 0).astype(bool),
        (df['percentage_im'] == 0).astype(bool),
        (df['percentage_fm'] == 0).astype(bool),
        (df['coef2'] > 0.2).astype(bool),
        (df['coef2'] < -0.2).astype(bool),
            ]
    choices = ['??', 'fin', 'ini', 'fin', 'ini']
    df['pos_tendency'] = np.select(conditions, choices, default='neut')

    return df

def main():

    df = dfq2()
    df_agg2 = aggregate(df.copy())

    df = df[mask1(df)]    
    df = df[mask2(df)]

    # Pre-aggregation
    df = df.sort_values(by=['gismu_freq', 'gismu'], ascending=[False, True])
    df = get_frequency_order(df)

    # Pivot
    cols = ('cmavo_rafsi', 'coef1', 'form_shape', 'rafsi_pos')
    dfs = (df.pivot(values=col, index='gismu', columns='frequency_order')
            .add_prefix(f'{col}_') for col in cols)
    df = pd.concat(dfs, axis=1)

    # Merge dfq1 and meaning
    dfquery1 = dfq1().set_index('gismu') 
    df_agg2 = df_agg2.set_index('gismu') 
    df = pd.concat([df, dfquery1, df_agg2], axis=1)
    df = df.reset_index()

    df['gismu_shape'] = df['gismu'].apply(word_shape)
    df = determine_pos_tendency(df)
    df = inserts.insert_meanings(df)
  
    # Process candidate forms
    from src.process_candidate_form import process_candidate_form

    cols = ['cmavo_rafsi_1', 'form_shape_1', 'gismu', 'gismu_shape', 'rafsi_pos']
    data = df[cols].fillna('').values.tolist()     # values 'turn' df into np
    data_processed = [process_candidate_form(*row) for row in tqdm(data, desc='Processing candidates')]
    df['processed'] = pd.Series(data_processed)
    
    df = df.sort_values(by=['gismu_shape', 'gismu_sum'], ascending=[True, False])
    df = df[['gismu', 'processed',
            'cmavo_rafsi_1', 'cmavo_rafsi_2', 'cmavo_rafsi_3', 'excluded',
            'coef1_1', 'coef1_2', 'coef1_3',
            'form_shape_1', 'form_shape_2', 'form_shape_3',
            'rafsi_pos_1', 'rafsi_pos_2', 'rafsi_pos_3',
            'rafsi_pos', 'gismu_sum', 'pos_tendency', 'meaning']]
    df.to_csv('results/df3b.csv', sep=',', index=False)
    return df
