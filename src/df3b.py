import numpy as np
import pandas as pd
from tqdm import tqdm

import src.inserts as inserts
import config.threshholds as th
import config.misc as config_misc
from src.df1_q1 import main as dfq1
from src.df1_q2 import main as dfq2
from src.classes.table import Table
from src.df3_shared import determine_pos_tendency
from src.lojban_specific.word_shape import word_shape
from src.lojban_specific.parser import syllable_parser
from src.df3b_dependencies.process_candidate_form import stages
from src.df3b_dependencies.handle_duplicates import handle_duplicate_df
from src.df3b_dependencies.classes import Row
import src.newlang_specific.sound_changes as sound_changes
import src.df3b_dependencies.override as override

def get_frequency_order(df):
    df['frequency_order'] = df.groupby('gismu')['gismu'].cumcount() + 1
    return df

def mask1a(df):
    return df['coef1'] > th.coef1_threshhold
def mask1b(df):
    return ~df['rafsi_pos'].str.contains('_')
def mask1(df):
    return mask1a(df) & mask1b(df)
def mask2(df):
    return (df['cmavo_rafsi'].str.len() != 5)

def aggregate(df):
    mask_a, mask_b = mask1a(df), mask1b(df)
    mask = mask1(df)
    df2 = df.copy()
    df2['form_len'] = df2['rafsi_pos'].str.len()
    df2 = df2.sort_values(by=['form_len', 'rafsi_pos'])

    df = df.assign(
                excluded_a=df['cmavo_rafsi'].where(~mask_a, ''),
                excluded_b=df['cmavo_rafsi'].where(~mask_b, ''),
            ).groupby('gismu', as_index=False).agg(
                excluded_a=('excluded_a', ' '.join),
                excluded_b=('excluded_b', ' '.join),
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
    cols = ['as_rafsi', '%_im', '%_fm', 'coef2']

    # Sanitisation
    for col in cols:
        df[col] = (pd.to_numeric(df[col], errors='coerce')
        .replace(np.inf, 999)
        .replace(-np.inf, -999)
        )

    df[cols] = df[cols].fillna(0)

    conditions = [
        (df['as_rafsi'] == 0).astype(bool),
        (df['%_im'] == 0).astype(bool),
        (df['%_fm'] == 0).astype(bool),
        (df['coef2'] > 0.2).astype(bool),
        (df['coef2'] < -0.2).astype(bool),
            ]
    choices = ['??', 'fin', 'ini', 'fin', 'ini']
    df['pos_tendency'] = np.select(conditions, choices, default='neut')

    return df

def process_candidates(df):

    def generate_counts(df2, col):
        mask1 = df2[col].isna()
        mask2 = df2[col] == ''
        mask = ~mask1 & ~mask2
        df2[f'n{col}'] = 0
        df2[f'n{col}'][mask] = (df2.groupby(col)[col].transform('count'))[mask]    
        return df2 

    df[df.select_dtypes(include='object').columns] = df.select_dtypes(include='object').fillna('')
    df[df.select_dtypes(include='number').columns] = df.select_dtypes(include='number').fillna(0)

    df2 = pd.DataFrame()
    counts, shapes = list(), list()

    data = df.to_dict('records')     # .values.tolist() ; values 'turn' df into np
    rows = [Row(d) for d in data]

    for i, stage in enumerate(stages):

        j = i + 1
        data = df.to_dict('records')     # .values.tolist() ; values 'turn' df into np

        if i == 0:
            data_forms = [stage(row) for row in rows]
        else:
            data_forms = [stage(row, c, sh) for (row, c, sh) in zip(rows, counts, shapes)]

        df2[f'c{j}'] = pd.Series(data_forms)
        df2 = generate_counts(df2, f'c{j}')
        counts = df2[f'nc{j}'].to_list()

        df['current_stem'] = df2[f'c{j}']
        df['current_stem_shape'] = df['current_stem'].apply(word_shape)
        shapes = df['current_stem_shape'].to_list()
    
    df = pd.concat([df, df2], axis=1) 

    return df

def main(override_file='update'):
    
    df = dfq2()
    df_agg2 = aggregate(df.copy())

    df = df[mask1(df)]    
    df = df[mask2(df)]

    # Pre-pivot
    df = df.sort_values(by=['gismu_freq', 'gismu'], ascending=[False, True])
    df = get_frequency_order(df)

    # Pivot
    cols = ('cmavo_rafsi', 'coef1', 'form_shape', 'rafsi_pos')
    dfs = (df.pivot(values=col, index='gismu', columns='frequency_order')
            .add_prefix(f'{col}_') for col in cols)
    df = pd.concat(dfs, axis=1)

    # Fetch defs_gismu index
    # dfg = Table('defs_gismu').dff
    # dfg = dfg.reset_index(names='gismu_index').set_index('gismu')
    # df = df.merge(dfg, on='gismu', how='left')

    # Merge dfq1 and meaning
    dfquery1 = dfq1().set_index('gismu') 
    df_agg2 = df_agg2.set_index('gismu') 
    df = pd.concat([df, dfquery1, df_agg2], axis=1)
    df = df.reset_index()

    # Fetch override
    df2 = override.get_df_override().reset_index()[['gismu', 'override', 'override_notes']]
    df = df.merge(df2, on='gismu', how='left')

    # Other ops
    df['gismu_shape'] = df['gismu'].apply(word_shape)
    df = determine_pos_tendency(df)
    df = inserts.insert_meanings(df)

    # current df columns
    all_cols = ['gismu', 'cmavo_rafsi_1', 'cmavo_rafsi_2', 'cmavo_rafsi_3', 'coef1_1',
       'coef1_2', 'coef1_3', 'form_shape_1', 'form_shape_2', 'form_shape_3',
       'rafsi_pos_1', 'rafsi_pos_2', 'rafsi_pos_3', 'gismu_shape', 'coef2',
       '%_im', '%_fm', 'gismu_sum', 
       'as_rafsi', 'as_gismu', 'as_cmavo', 
       '%_rafsi', '%_gismu', '%_cmavo',
       '%_ri', '%_rf',
       'theme_code', 'theme', 'excluded_a', 'excluded_b',
       'rafsi_pos', 'override', 'override_notes', 'pos_tendency', 'meaning']

    # Process candidate forms
    df = process_candidates(df)
    # df = handle_duplicate_df(df)

    def post_processing():
        df['current_stem_syllablfied'] = df['current_stem'].apply(lambda x : syllable_parser(x, delim='-'))
        # df['current_combining'] = df['current_stem'].apply(sound_changes.stem_to_combining)
        # df['current_lemma'] = df['current_stem'].apply(sound_changes.stem_to_lemma)
        # df['current_lemma_count'] = df.groupby('current_lemma')['gismu'].transform('count')
    post_processing()

    # Write to files
    print_cols = ['gismu', 
            'current_stem', 'current_stem_shape', 
            'current_stem_syllablfied',
            'cmavo_rafsi_1', 'cmavo_rafsi_2', 'form_shape_1', 'form_shape_2',
            'meaning', 'pos_tendency', 'override', 
            'c1', 'nc1',
            'gismu_sum', 
            '%_ri', '%_rf',
            '%_rafsi', '%_gismu', '%_cmavo',
        ]
    df_out = df[print_cols]
    df_out.to_csv('results/df3b1.csv', sep=',', index=False)

    # cols2 = ['theme_code', 'gismu', 'current_stem', 'current_lemma', 'current_combining', 'meaning', 'gismu', 'override', 'override_notes']
    # df[cols2].to_csv('results/df3b2.csv', sep=',', index=False)

    if override_file == 'new':
        override.create_new_override(df)
    elif override_file == 'update':
        override.update_override_file(df)
    elif override_file == 'copy':
        override.copy_override_into_file(df)
        
    return df
