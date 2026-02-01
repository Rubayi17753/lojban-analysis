# Computes percentages
# Checks how much gismu (and variant forms) are inclined towards being lujvo-initial or final

import math
import numpy as np 
from src.df1 import create_grand_table 
from src.lojban_specific.word_shape import word_shape

def main(filter=1):

    df = create_grand_table()

    cols = ('as_gismu', 
            'as_rafsi_conv', 'as_rafsi_i', 'as_rafsi_m', 'as_rafsi_f', 
            'as_cmavo', 'as_cmavo_compound', )
    df = (df.groupby('gismu', as_index=False)
            .agg({col: 'sum' for col in cols}))

    df['word_length'] = df['gismu'].str.len()
    df = df[df['word_length'] == 5]

    df['gismu_shape'] = df['gismu'].apply(word_shape)
    df['as_rafsi'] = df['as_rafsi_i'] + df['as_rafsi_m'] + df['as_rafsi_f']

    df['as_rafsi_im'] = df['as_rafsi_i'] + df['as_rafsi_m']
    df['as_rafsi_fm'] = df['as_rafsi_f'] + df['as_rafsi_m']
    df['%_im'] = round( df['as_rafsi_im'] / df['as_rafsi'] * 100 , 1)
    df['%_fm'] = round( df['as_rafsi_fm'] / df['as_rafsi'] * 100 , 1)

    df['coef2'] = np.log10(df['%_fm'] / df['%_im'])
    df['coef2'] = round( df['coef2'] * (1 - df['as_rafsi'] ** -0.5) , 2) # penalty for low rafsi attestation

    df['as_cmavo'] = df['as_cmavo'] + df['as_cmavo_compound']
    df['gismu_sum'] = df['as_gismu'] + df['as_rafsi'] + df['as_cmavo']

    df['%_rafsi'] = round( df['as_rafsi'] / df['gismu_sum'] * 100 , 1)
    df['%_cmavo'] = round( df['as_cmavo'] / df['gismu_sum'] * 100 , 1)
    df['%_gismu'] = round( df['as_gismu'] / df['gismu_sum'] * 100 , 1)

    df['%_ri'] = round( df['%_im'] * df['%_rafsi'] / 100, 1)
    df['%_rf'] = round( df['%_fm'] * df['%_rafsi'] / 100, 1)
    
    df = df[['gismu', 'gismu_shape', 'coef2', 
                '%_im', '%_fm', 
                '%_ri', '%_rf', 
                'gismu_sum',
                'as_rafsi_im', 'as_rafsi_fm',
                'as_rafsi', 'as_gismu', 'as_cmavo',
                '%_rafsi', '%_gismu', '%_cmavo',
                ]]

    df = df.sort_values('coef2')

    if filter:
        from src.custom_excludes import exclude_classes
        df = exclude_classes(df)

    df.to_csv('results/df1_q1.csv', sep=',', index=False)
    return df
