import numpy as np
import pandas as pd
import src.inserts as inserts
from src.df1_q1 import main as dfq1
from src.df1_q2 import main as dfq2

def filter_and_aggregate(df):

    mask = (
        df['coefficient'] > 2   # Coefficient here: q2's df['form_freq'] / df['max_form_freq'] * 100
    )

    df = df.assign(
                include=df['cmavo_rafsi'].where(mask, ' '),
                exclude=df['cmavo_rafsi'].where(~mask, ' '),
            ).groupby('gismu', as_index=False).agg(
                forms_included=('include', ' '.join),
                forms_excluded=('exclude', ' '.join),
    )

    return df

def determine_pos_tendency(df):
    # Determine rafsi positioning tendency.
    # Requires dfq1() --> log(fin/ini)
    # The 'raw' coefficients get 'penalised' for low rafsi attestations

    # Sanitisation

    df = df.copy()

    for col in ('as_rafsi', 'percentage_im', 'percentage_fm', 'log(fin/ini)'):
        df[col] = (pd.to_numeric(df[col], errors='coerce')
        .replace(np.inf, 999)
        .replace(-np.inf, -999)
        )

    df = df.fillna(0)

    conditions = [
        (df['as_rafsi'] == 0).astype(bool),
        (df['percentage_im'] == 0).astype(bool),
        (df['percentage_fm'] == 0).astype(bool),
        (df['log(fin/ini)'] > 0.25).astype(bool),
        (df['log(fin/ini)'] < -0.25).astype(bool),
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

    # Post-aggregation
    df = df.merge(dfq1(),
            on='gismu', how='left')

    df = determine_pos_tendency(df)
    df = df.sort_values(by=['gismu_shape', 'as_rafsi'], ascending=[True, False])
    df = df[['gismu', 'pos_tendency', 'forms_included', 'forms_excluded']]
    df = inserts.insert_meanings(df)
    df.to_csv('results/df3.csv', sep=',', index=False)
    return df
