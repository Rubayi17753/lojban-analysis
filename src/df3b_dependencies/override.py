import pandas as pd
from src.classes.table import Table
from src.lojban_specific.word_shape import word_shape

override_fp = 'interactive/new_gismu.csv'

def get_df_override():
    df = pd.read_csv(override_fp, index_col='gismu')
    df[df['override'] == '_']['override'] = None
    return df

def create_new_override(df):

    from src.lojban_specific.meanings_gismu import get_df_gismu_meaning

    df['override'] = ''
    df['final_count'] = df.groupby('current_stem')['gismu'].transform('count')
    df = Table('defs_gismu').dff[['gismu', 'theme_code']].merge(df, on='gismu', how='right')

    df = df.sort_values('theme_code')
    df = df[['gismu', 'current_stem', 'override', 'notes', 'current_stem_count', 'pos_tendency', 'theme_code', 'meaning']]
    df.to_csv(override_fp, index=False)

def override_generated_forms(df):
    df = df.set_index('gismu')
    df['override'] = get_df_override()['override']
    # override if not NaN, else current_stem
    df['form_overridden'] = df['current_stem'].copy()
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
    b = df[['current_stem', 'final_count', 'pos_tendency']]
    df_override = (pd.concat([a, b], axis=1))
    df_override = df_override[['current_stem', 'override', 'notes', 'final_count',
                     'pos_tendency', 'theme_code', 'meaning']]
    df_override.reset_index().to_csv('interactive/new_gismu.tsv', index=False)

def copy_override_into_file(df):

    df[df['override'].isna()]['override'] = '_'
    df[df['override_notes'].isna()]['override_notes'] = '_'
    df[df['override'] == '']['override'] = '_'
    df[df['override_notes'] == '']['override_notes'] = '_'

    # Sort based on defs_gismu (thematic)
    df_defs_gismu = Table('defs_gismu', keep_default_na=False, sep=',').dff
    df = df_defs_gismu[['gismu']].merge(df, on='gismu', how='left')

    cols2 = ['theme_code', 'gismu', 'meaning', 'gismu', 'override', 'override_notes']
    # 'current_stem', 'current_lemma', 'current_combining', 
    df[cols2].to_csv(override_fp, index=False)