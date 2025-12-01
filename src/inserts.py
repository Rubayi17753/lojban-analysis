# Insert columns from base and apply functions to columns
from src.tools.class_table import Table

def insert_shapes(df):

    from src.lojban_specific.word_shape import word_shape
    df['gismu_shape'] = df['gismu'].apply(word_shape)
    df['form_shape'] = df['cmavo_rafsi'].apply(word_shape)

    return df

def insert_meanings(df):
    
    from src.lojban_specific.rafsi_meanings import get_df_rafsi_meaning
    df = df.merge(get_df_rafsi_meaning(),
                left_on='gismu', right_on='rafsi', how='left')
    df = df.drop(columns='rafsi')
    return df

def insert_rafsi_pos(df):

    from src.substring_positions import substring_positions
    df['cmavo_rafsi2'] = df['cmavo_rafsi'].str.replace("'", '')
    df['rafsi_pos'] = df.apply(lambda x: substring_positions(x['gismu'], x['cmavo_rafsi2'], 
                                                            out='string', delim=''), 
                                                            axis=1)
    df['rafsi_pos'] =  df['rafsi_pos'].str.replace('  ', ' ')
    df = df.drop(columns=['cmavo_rafsi2'])

    # df = df.merge(Table('pos_substitutions').dff,left_on='rafsi_pos', right_on='old_pos', how='left')
    # df = df.rename(columns={'new_pos': 'rafsi_pos_new'})
    # df['rafsi_pos_new'] =  df['rafsi_pos_new'].str.replace(' ', '')                 
    return df
