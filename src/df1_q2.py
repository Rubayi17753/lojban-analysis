# Rafsi data

from src.df1 import create_grand_table 

def insert_shapes(df):

    from src.lojban_specific.word_shape import word_shape
    df['gismu_shape'] = df['gismu'].apply(word_shape)
    df['form_shape'] = df['cmavo_rafsi'].apply(word_shape)

    return df

def insert_thematic(df):

    from src.tools.class_table import Table
    df1 = Table('defs_gismu').dff[['gismu', 'theme_code']]
    df2 = Table('themes_gismu').dff[['theme_code', 'theme']]

    df1 = df1.merge(df2, on='theme_code', how='left')
    df = df.merge(df1, on='gismu', how='left')

    return df

def insert_meanings(df):
    
    from src.lojban_specific.rafsi_meanings import get_df_rafsi_meaning
    df = df.merge(get_df_rafsi_meaning(),
                left_on='cmavo_rafsi', right_on='rafsi', how='left')
    return df

def exclude_classes(df):
    excludeds = ['7.4.3', # SI prefixes
                '7.5.4', # chemical elements
                '12.2', '12.3', '12.4', '12.5.1', # ethnocultural & religious
                ]
    return df[~df['theme_code'].isin(excludeds)]

def main():

    df = create_grand_table()
    df = insert_thematic(df)
    df = exclude_classes(df)
    df = insert_shapes(df)
    df = insert_meanings(df)

    df = df.drop_duplicates()

    cols = ['as_gismu', 
            'as_rafsi_conv', 'as_rafsi_i', 'as_rafsi_m', 'as_rafsi_f', 
            'as_cmavo', 'as_cmavo_compound', 
            'form_freq', ]

    cols2 = ['sum_gismu', 
            'sum_rafsi_conv', 'sum_rafsi_i', 'sum_rafsi_m', 'sum_rafsi_f', 
            'sum_cmavo', 'sum_cmavo_compound', 
            'gismu_freq', ]

    df['form_freq'] = sum((df['as_gismu'], 
                       df['as_rafsi_conv'], df['as_rafsi_i'], df['as_rafsi_m'], df['as_rafsi_f'], 
            df['as_cmavo'], df['as_cmavo_compound'], ))

    df['gismu_freq'] = df.groupby('gismu')['form_freq'].transform('sum')
    df['max_form_freq'] = df.groupby('gismu')['form_freq'].transform('max')
    df['coefficient'] = round(df['form_freq'] / df['max_form_freq'] * 100 , 1)

    df['word_length'] = df['gismu'].str.len()
    df = df[df['word_length'] == 5]
    df = df.sort_values(by=['gismu_freq', 'gismu', 'form_freq'], ascending=[False, True, False])

    df.to_csv('results/df1_q2.csv', sep=',', index=False)
    return df
