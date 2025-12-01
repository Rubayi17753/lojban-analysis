# Rafsi data

import src.inserts as inserts
from src.df1 import create_grand_table 
from src.tools.class_table import Table

def main(filter=1):

    df = create_grand_table()

    if filter:
        from src.custom_excludes import exclude_classes
        df = exclude_classes(df)

    df = inserts.insert_shapes(df)
    df = inserts.insert_meanings(df)
    df = inserts.insert_rafsi_pos(df)

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
