from src.tools.class_table import Table

def insert_thematic(df):

    df1 = Table('defs_gismu').dff[['gismu', 'theme_code']]
    df2 = Table('themes_gismu').dff[['theme_code', 'theme']]

    df1 = df1.merge(df2, on='theme_code', how='left')
    df = df.merge(df1, on='gismu', how='left')

    return df

def exclude_classes(df):

    df = insert_thematic(df)
    excludeds = ['7.4.3', # SI prefixes
                '7.5.4', # chemical elements
                '12.2', '12.3', '12.4', '12.5.1', # ethnocultural & religious
                ]
    df = df[~df['theme_code'].isin(excludeds)]

    brods = ['broda', 'brode', 'brodi', 'brodo', 'brodu']
    df = df[~df['gismu'].isin(brods)]

    return df