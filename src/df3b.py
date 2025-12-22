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

def get_df_override():
    return pd.read_csv('interactive/new_gismu.tsv', sep='\t', index_col='gismu')

def get_frequency_order(df):
    df['frequency_order'] = df.groupby('gismu')['gismu'].cumcount() + 1
    return df

def mask1(df):

    excludeds = ("a'a", "e'e", "i'i", "o'o", "u'u",
                "ei", "e'i", "o'u")
    mask = (
        (df['coef1'] > th.coef1_threshhold) &   # Coefficient here: q2's df['cmavo_rafsi_freq'] / df['max_form_freq'] * 100
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
    df = Table('defs_gismu').dff[['gismu', 'theme_code']].merge(df, on='gismu', how='right')

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

def process_candidates(df):
    from src.process_candidate_form import stage1

    # cols = ['cmavo_rafsi_1', 'form_shape_1', 'gismu', 'gismu_shape', 'rafsi_pos']

    df[df.select_dtypes(include='object').columns] = df.select_dtypes(include='object').fillna('')
    df[df.select_dtypes(include='number').columns] = df.select_dtypes(include='number').fillna(0)

    data = df.to_dict('records')     # .values.tolist() ; values 'turn' df into np
    data_forms = [stage1(row) for row in tqdm(data, desc='Processing candidates')]
  
    df2 = pd.DataFrame(data_forms)   
    
    print(df2)
    exit()

    new_cols = [x for x in df2.columns if x != 'stack'] + ['stack']
    df2 = df2[new_cols]

    # Applies only if ordered == 1 (see process_candidate_form.stage1)
    if df2.columns[0] == 0:
        df2 = df2.rename(columns=lambda n: f'form_{n}')
  
    for col in list((x for x in df2.columns if x != 'form_stack')):
        mask1 = df2[col].isna()
        mask2 = df2[col] == ''
        mask = ~mask1 & ~mask2
        df2[f'{col}_n'] = 0
        df2[f'{col}_n'][mask] = (df2.groupby(col)[col].transform('count'))[mask]
    df = pd.concat([df, df2], axis=1) 

    data_forms2 = [stage1(row, index_by='form_type') for row in tqdm(data, desc='Processing candidates')]
    df2b = pd.DataFrame(data_forms2)
    df = pd.concat((df, df2b), axis=1)

    # df['current_form_shape'] = df['current_form'].apply(word_shape)
    # df['max_coef'] = df.groupby('form_overridden')['coef1_1'].transform('max')
    # df['coef3'] = round( df['coef1_1'] / df['max_coef'] , 2)

    return df

def handle_duplicate_forms(df, display_stats=1, sift=1):
    df['current_form_count'] = df.groupby('current_form')['gismu'].transform('count')
    mask_dupl = df['current_form_count'] > 1

    if display_stats:
        dupl_count = mask_dupl.sum()
        print(f'Duplicates remaining: {dupl_count}\n')

        df['current_form_shape'] = df['current_form'].apply(word_shape)
        print('Form shape rundown: ')
        print(df['current_form_shape'].value_counts())

    df['max_gismu_sum'] = df.groupby('current_form')['gismu_sum'].transform('max')
    df['coef_gismu_sum'] = df['gismu_sum'] / df['max_gismu_sum']

    gismus = list(df['gismu'])
    current_forms = list(df['current_form'])
    form_stacks = list(df['form_stack'])
    coefs = list(df['coef_gismu_sum'])
    tendencies = list(df['pos_tendency'])
    # set_current_forms = set(current_forms)

    def conditions(stack, dupl, coef, tendency):
        if sift == 1:
            return stack and dupl and coef < 0.8
        elif sift == 10:
            return stack and dupl and coef < 0.99
        elif sift == 2:
            return stack and dupl
        elif sift == 3:
            return (stack and dupl and  
                    (
                        (tendency == 'ini' and word_shape(stack[-1])[:2] == 'CC')
                        or (tendency == 'fin' and word_shape(stack[-1])[-2:] == 'CC')
                    ))

    cur_forms, stacks = list(), list()
    n_changes = 0
    for g, cur_form, stack, dupl, coef, tendency in zip( gismus, current_forms, form_stacks, mask_dupl, coefs, tendencies ):
        if conditions(stack, dupl, coef, tendency):
            cur_form = stack.pop()
            n_changes += 1
        cur_forms.append(cur_form)
        stacks.append(stack)

    if display_stats:
        print(f'{n_changes} forms changed')

    df['current_form'] = pd.Series(cur_forms)
    df['form_stack'] = pd.Series(stacks)
    df['current_form_count'] = df.groupby('current_form')['gismu'].transform('count')

    return df

def handle_duplicate_df(df):

    df['current_form'] = df['form_0']
    df = handle_duplicate_forms(df)
    df = handle_duplicate_forms(df, sift=3)
    df = handle_duplicate_forms(df)
    for i in range(4):
        df = handle_duplicate_forms(df, sift=10)
    for i in range(4):
        df = handle_duplicate_forms(df, sift=2)
    
    return df

def main(override_file='update'):
    
    import src.process_candidate_form as process_candidate_form

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

    # Fetch override
    df2 = get_df_override().reset_index()[['gismu', 'override']]
    df = df.merge(df2, on='gismu', how='left')

    # Other ops
    df['gismu_shape'] = df['gismu'].apply(word_shape)
    df = determine_pos_tendency(df)
    df = inserts.insert_meanings(df)
  
    # Process candidate forms
    df = process_candidates(df)
    df = handle_duplicate_df(df)

    # Post-processing
    df['current_shape'] = df['current_form'].apply(word_shape)

    # Write to files
    print(df.columns)
    df.to_csv('results/df3b1.csv', sep=',', index=False)

    df[['gismu', 'current_form', 'meaning']].to_csv('results/df3b2.csv', sep=',', index=False)

    col_shapes = process_candidate_form.cols
    col_forms = ['form_0', 'form_1', 'form_2', 'form_3', 'form_4', 'form_5',]
    initial_forms = ['cmavo_rafsi_1', 'cmavo_rafsi_2', 'cmavo_rafsi_3', 'excluded',]
    df[['gismu', 'pos_tendency', 'gismu_sum', 'current_form', 'current_shape', 'current_form_count', 'meaning', 
    *col_forms, *col_shapes, *initial_forms, ]].to_csv('results/df3b3.csv', sep=',', index=False)

    if override_file == 'new':
        create_new_override(df)
    elif override_file == 'update':
        update_override_file(df)

    return df
