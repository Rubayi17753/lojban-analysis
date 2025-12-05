import numpy as np
import pandas as pd
from tqdm import tqdm
import src.inserts as inserts
from src.df1_q1 import main as dfq1
from src.df1_q2 import main as dfq2
from src.tools.class_table import Table
from src.df3_shared import determine_pos_tendency
from src.lojban_specific.word_shape import word_shape

def get_df_override():
    return pd.read_csv('interactive/new_gismu.tsv', sep='\t', index_col='gismu')

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

def create_new_override(df):

    from src.lojban_specific.meanings_gismu import get_df_gismu_meaning

    df['override'] = ''
    df['final_count'] = df.groupby('current_form')['gismu'].transform('count')
    df = df.merge(Table('defs_gismu').dff[['gismu', 'theme_code']], on='gismu', how='left')

    df = df.sort_values('theme_code')
    df = df[['gismu', 'current_form', 'override', 'notes', 'current_form_count', 'pos_tendency', 'theme_code', 'meaning']]
    df.to_csv('interactive/new_gismu.tsv', sep='\t', index=False)

def override_generated_forms(df):
    df = df.set_index('gismu')
    df['override'] = get_df_override()['override']
    # override if not NaN, else current_form
    df['form_overridden'] = df['current_form'].copy()
    df.loc[~df['override'].isna(), 'form_overridden'] = df['override']
    df = df.reset_index()
    df['final_count'] = df.groupby('form_overridden')['gismu'].transform('count')
    df['final_shape'] = df['form_overridden'].apply(word_shape)
    return df

def update_override_file(df):
    # Reads new_gismu, then feeds pandas-generated columns onto it
    df = df.set_index('gismu')
    df_override = get_df_override()

    cols = list(col for col in list(df_override.columns) if col not in ('gismu', 'override', 'theme_code'))
    cols.append('final_count')

    a = df_override[['override', 'theme_code', 'meaning', 'notes']]
    b = df[['current_form', 'final_count', 'pos_tendency']]
    df_override = (pd.concat([a, b], axis=1))
    df_override = df_override[['current_form', 'override', 'notes', 'final_count',
                     'pos_tendency', 'theme_code', 'meaning']]
    df_override.reset_index().to_csv('interactive/new_gismu.tsv', sep='\t', index=False)

def main(override_file='update'):

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
    from src.process_candidate_form import stage1, stage2

    # cols = ['cmavo_rafsi_1', 'form_shape_1', 'gismu', 'gismu_shape', 'rafsi_pos']

    df[df.select_dtypes(include='object').columns] = df.select_dtypes(include='object').fillna('')
    df[df.select_dtypes(include='number').columns] = df.select_dtypes(include='number').fillna(0)

    data = df.to_dict('records')     # .values.tolist() ; values 'turn' df into np
    data_current_form = [stage1(row) for row in tqdm(data, desc='Processing candidates')]
    df['current_form'] = pd.Series(data_current_form)
    df['current_form_shape'] = df['current_form'].apply(word_shape)
    if override_file == 'update':
        df = override_generated_forms(df)
    
    data = df.to_dict('records')
    data_current_form = [stage2(row) for row in tqdm(data, desc='Processing candidates')]
    df['current_form'] = pd.Series(data_current_form)
    df['current_form_shape'] = df['current_form'].apply(word_shape)
    if override_file == 'update':
        df = override_generated_forms(df)

    df = df.sort_values(by=['form_overridden', 'gismu_sum'], ascending=[True, False])
    df = df[['gismu', 'gismu_shape', 
            'current_form', 'override', 'final_shape', 'final_count',
            'pos_tendency',
            'cmavo_rafsi_1', 'cmavo_rafsi_2', 'cmavo_rafsi_3', 'excluded',
            'coef1_1', 'coef1_2', 'coef1_3',
            'form_shape_1', 'form_shape_2', 'form_shape_3',
            'rafsi_pos_1', 'rafsi_pos_2', 'rafsi_pos_3',
            'rafsi_pos', 'gismu_sum', 'meaning']]
    df.to_csv('results/df3b.csv', sep=',', index=False)

    if override_file == 'new':
        create_new_override(df)
    elif override_file == 'update':
        update_override_file(df)

    return df
