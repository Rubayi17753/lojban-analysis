# Checks how much gismu (and variant forms) are inclined towards being lujvo-initial or final

from src.df1 import create_grand_table 

def main():

    df = create_grand_table()

    cols = ('as_gismu', 
            'as_rafsi_conv', 'as_rafsi_i', 'as_rafsi_m', 'as_rafsi_f', 
            'as_cmavo', 'as_cmavo_compound', )
    df = (df.groupby('gismu', as_index=False)
            .agg({col: 'sum' for col in cols}))

    df['word_length'] = df['gismu'].str.len()
    df = df[df['word_length'] == 5]

    df['as_rafsi'] = df['as_rafsi_i'] + df['as_rafsi_m'] + df['as_rafsi_f']
    df['percentage_im'] = round( (df['as_rafsi_i'] + df['as_rafsi_m']) / df['as_rafsi'] * 100 , 1)
    df['percentage_fm'] = round( (df['as_rafsi_f'] + df['as_rafsi_m']) / df['as_rafsi'] * 100 , 1)
    df['fin/ini'] = round( df['percentage_fm'] / df['percentage_im'] , 2)
    df['as_cmavo'] = df['as_cmavo'] + df['as_cmavo_compound']
            
    df = df[['gismu', 'fin/ini', 
                'percentage_im', 'percentage_fm', 
                'as_rafsi', 'as_gismu', 'as_cmavo']]

    df = df.sort_values('fin/ini')

    df.to_csv('results/df1_q1.csv', sep=',', index=False)
    return df
