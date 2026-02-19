import numpy as np
import pandas as pd
from tqdm import tqdm

import src.inserts as inserts
import config.threshholds as th
import config.misc as config_misc
from src.df1_q1 import main as dfq1
from src.df1_q2 import main as df1_q2
from src.classes.table import Table
from src.df3_shared import determine_pos_tendency
from src.lojban_specific.word_shape import word_shape
from src.lojban_specific.parser import syllable_parser
from src.df3b_dependencies.process_candidate_form import stages, stages_param
from src.df3b_dependencies.handle_duplicates import handle_duplicate_df
from src.df3b_dependencies.classes import Row
import src.newlang_specific.sound_changes as sound_changes
import src.df3b_dependencies.override as override

def get_frequency_order(df):
    df['frequency_order'] = df.groupby(['gismu', 'form_category'])['gismu'].cumcount() + 1
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

def rank_stats(df):

    df = df[['current_stem', '%_ri', '%_rf', 'coef2',]]

    df['max_%_ri'] = df.groupby('current_stem')['%_ri'].transform('max')
    df['max_%_rf'] = df.groupby('current_stem')['%_rf'].transform('max')
    df['max_coef2'] = df.groupby('current_stem')['coef2'].transform('max')
    df['ri_rank'] = df['%_ri'] / df['max_%_ri']
    df['rf_rank'] = df['%_rf'] / df['max_%_rf']
    df['coef2_rank'] = df['coef2'] / df['max_coef2']
    # print(df[['current_stem', 'coef2', 'max_coef2', 'coef2_rank']])

    return df

def process_candidates(df):

    df[df.select_dtypes(include='object').columns] = df.select_dtypes(include='object').fillna('')
    df[df.select_dtypes(include='number').columns] = df.select_dtypes(include='number').fillna(0)

    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    counts, shapes = list(), list()
    df['current_stem'] = ''

    data = df.to_dict('records')     # .values.tolist() ; values 'turn' df into np
    rows = [Row(d) for d in data]
    osfs = [d['%_cmavo'] > 20 
        or (d['as_rafsi_im'] > 150 and d['%_ri'] > 10)
        or (d['as_rafsi_fm'] > 150 and d['%_rf'] > 10)
        for row, d in zip(rows, data)]   # oblige short forms

    for i, (stage, stage_param) in enumerate(zip(stages, stages_param)):
        
        if not stage_param:
            stage_param = dict()

        j = i + 1
        data = df.to_dict('records')     # .values.tolist() ; values 'turn' df into np

        if i == 0:
            data_forms = [stage(row) for row in rows]
        else:
            list_previous_forms = list(c if c else '' for c in df['current_stem'].to_list())
            set_previous_forms = set(c for c in data_forms.copy() if c)
            data_forms = [stage(row, c, sh, prev, ri, rf, rcoef2, osf) 
                            for (row, c, sh, prev, ri, rf, rcoef2, osf) 
                            in zip(rows, counts, shapes, 
                            list_previous_forms,
                            list_ri_rank, list_rf_rank, list_rcoef2_rank,
                            osfs)]          
            
            if stage_param.get('purge_forms_already_used', 1):
                data_forms = [c if c not in set_current_stems else '' for c in data_forms]

        df2[f'c{j}'] = pd.Series(data_forms)

        # Replace current_stem with entries from df2 where not empty
        df['current_stem'] = df2[f'c{j}'].where(df2[f'c{j}'] != '', df['current_stem'])
        df['current_stem_shape'] = df['current_stem'].apply(word_shape)

        rank_df = rank_stats(df)[['ri_rank', 'rf_rank', 'coef2_rank']]
        list_ri_rank = rank_df['ri_rank'].to_list()
        list_rf_rank = rank_df['rf_rank'].to_list()
        list_rcoef2_rank = rank_df['coef2_rank'].to_list()
        
        df[['ri_rank', 'rf_rank', 'coef2_rank']] = rank_df[['ri_rank', 'rf_rank', 'coef2_rank']]
        rank_df.columns = [f'rank_i{j}', f'rank_f{j}', f'rank_coef2{j}']
        df3 = pd.concat([df3, rank_df], axis=1) 

        set_current_stems = set(df['current_stem'].to_list())

        def generate_counts():
            # mask1 = df['current_stem'].isna()
            # mask2 = df['current_stem'] == ''
            # mask = ~mask1 & ~mask2
            serie = (df.groupby('current_stem')['current_stem'].transform('count'))
            # serie[mask] = 0               
            return serie  

        serie = generate_counts()
        df2[f'nc{j}'] = serie
        counts = serie.to_list()

        shapes = df['current_stem_shape'].to_list()

    df = pd.concat([df, df2, df3], axis=1) 
    return df, df2.columns, df3.columns

def main(df1_q2, summary_fp, override_file='update'):
    
    df = df1_q2

    curr_columns = ['gismu', 'cmavo_rafsi', 'class', 'as_gismu', 'as_rafsi_conv',
       'as_rafsi_i', 'as_rafsi_m', 'as_rafsi_f', 'as_cmavo',
       'as_cmavo_compound', 'theme_code', 'theme', 'gismu_shape', 'form_shape',
       'meaning', 'rafsi_pos', 'form_freq', 'gismu_freq', 'max_form_freq',
       'coef1', 'word_length']

    df_agg2 = aggregate(df.copy())

    # df = df[mask1(df)]    # rafsi/form filter
    # df = df[mask2(df)]  # cmavo_rafsi length < 5

    # Determine category

    df['as_rafsi'] = df['as_rafsi_i'] + df['as_rafsi_m'] + df['as_rafsi_f']
    
    df['form_category'] = df['form_shape'].copy()
    mask = ((df['as_rafsi'] + df['as_gismu']) == 0)    # & df['class'].notna()
    df.loc[mask, 'form_category'] = 'cmavo'
    df.loc[df['form_category'].isin(('CACCA', 'CCACA')), 'form_category'] = 'f5'
    df.loc[df['form_category'].isin(('CACC', 'CCAC')), 'form_category'] = 'f4'
    
    # Pre-pivot
    df = df.sort_values(by=['gismu_freq', 'gismu'], ascending=[False, True])
    
    df = get_frequency_order(df)
    df.loc[df['frequency_order'] == 1, 'frequency_order'] = ''
    df.loc[df['frequency_order'] == 2, 'frequency_order'] = '2'   
    df['form_category'] = df['form_category'] + df['frequency_order']

    # Pivot
    cols = ('cmavo_rafsi', 'form_freq', 'rafsi_pos')    # 'coef1',   
    dfs = (df.pivot(values=col, index='gismu', columns=['form_category'])   # , 'frequency_order'
            # .add_prefix(f'{col}_') 
            for col in cols
            )
    df = pd.concat(dfs, axis=1)

    df.to_csv('results/df3c.csv', sep=',', index=False)
    exit()

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

    df.to_csv('results/df3c.csv', sep=',', index=False)        
    return df
