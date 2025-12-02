import numpy as np
import pandas as pd
import src.inserts as inserts
from src.df1_q1 import main as dfq1
from src.df1_q2 import main as dfq2
from src.tools.class_table import Table

def filters(df):

    mask = (
        (df['coef1'] > 2)   # Coefficient here: q2's df['cmavo_rafsi_freq'] / df['max_form_freq'] * 100
        & (~df['rafsi_pos'].str.contains('_'))
    )
    return mask

def filter_and_aggregate(df):

    mask = filters(df)
    df = df.assign(
                form=df['cmavo_rafsi'].where(mask, ' '),
                form_x=df['cmavo_rafsi'].where(~mask, ' '),
                rafsi_pos=df['rafsi_pos'].where(mask, ' '),
                form_shape=df['form_shape'].where(mask, ' '),
            ).groupby('gismu', as_index=False).agg(
                form=('form', ' '.join),
                form_x=('form_x', ' '.join),
                rafsi_pos=('rafsi_pos', ' '.join),
                form_shape=('form_shape', ' '.join),
    )

    df['rafsi_pos'] = df['rafsi_pos'].str.strip()
    df['form_shape'] = df['form_shape'].str.strip()

    return df

def produce_pivot(df):

    df = df[filters(df)]
    df2 = Table('defs_rafsi', keep_default_na=False).dff

    # Check if df.gismu/cmavo_rafsi is present in df2.gismu/rafsi. If not, designate as CAA2
    df2_index = df2.set_index(['gismu', 'rafsi']).index
    mask = df.set_index(['gismu', 'cmavo_rafsi']).index.isin(df2_index)
    mask2 = df['form_shape'].isin(['CACC', 'CCAC', 'CACCA', 'CCACA'])
    df.loc[~mask & ~mask2, 'form_shape'] = 'CAA2'

    # print(df[df.duplicated(subset=['gismu', 'form_shape'], keep=False)][['gismu', 'form_shape', 'cmavo_rafsi']])

    # df = df.pivot(index='gismu', columns='form_shape', values='cmavo_rafsi')
    df = df.pivot_table(values='cmavo_rafsi', index='gismu', columns='form_shape', aggfunc=(lambda x: ' '.join(x)))

    return df

def determine_pos_tendency(df):
    # Determine rafsi positioning tendency
    # Requires dfq1() --> coef2

    # Sanitisation

    for col in ('as_rafsi', 'percentage_im', 'percentage_fm', 'coef2'):
        df[col] = (pd.to_numeric(df[col], errors='coerce')
        .replace(np.inf, 999)
        .replace(-np.inf, -999)
        )

    df = df.fillna(0)

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

    # Pre-aggregation
    df = df.sort_values(by=['form_freq', 'gismu_freq'], ascending=[False, False])

    # Aggregation
    df = filter_and_aggregate(df)

    # Merge dfq1 and pivot(dfq2)
    df = df.merge(dfq1(),
            on='gismu', how='left').merge(produce_pivot(dfq2()),
            on='gismu', how='left')

    df = determine_pos_tendency(df)
    df = df.sort_values(by=['gismu_shape', 'as_rafsi'], ascending=[True, False])
    '''df = df[['gismu', 'gismu_shape', 
            'pos_tendency', 
            'form', 'form_x', 'rafsi_pos', 'form_shape']]'''
    df = inserts.insert_meanings(df)
    df.to_csv('results/df3.csv', sep=',', index=False)
    return df
