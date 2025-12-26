import pandas as pd
from src.classes.table import Table
import src.lojban_specific.phonological_inventory as inv
from src.lojban_specific.word_shape import word_shape
from src.lojban_specific.parser import lujvo_parser, determine_wordclass
from src.df_gismu_rafsi import get_df_gismu_rafsi

df_new_gismu = Table('new_gismu', 'interactive', keep_default_na=False, sep='\t').dff
dict_gismu_to_new = dict(zip(df_new_gismu['gismu'], df_new_gismu['current_form']))

# df_rafsi_to_gismu = Table('defs_rafsi', keep_default_na=False, sep=',').dff[['rafsi', 'gismu']]
df_rafsi_to_gismu = get_df_gismu_rafsi()
dict_rafsi_to_gismu = dict(zip(df_rafsi_to_gismu['rafsi'], df_rafsi_to_gismu['gismu']))

def translate_lujvo(lujvo, delim=''):

    x1 = 'f'
    x2 = '’'
    x3 = 'n'
    x4 = 'ṇ'
    
    def rafsi_to_gismu(s):
        if len(s) == 2:
            return s
        else:
            return dict_rafsi_to_gismu.get(s, f'[{s}]')

    def gismu_to_new(s):
        if len(s) < 5:
            s = f'<{s}>'
        else:
            s = dict_gismu_to_new.get(s, f'[{s}]')
        return s

    rafsis = lujvo_parser(lujvo, noisy=1)
    gismus = (rafsi_to_gismu(raf) for raf in rafsis)
    new_forms = [gismu_to_new(gis) for gis in gismus]
    shh = [word_shape(form) for form in new_forms]

    # insert hyphens/liaisons
    for i in range(len(new_forms) - 1):
        sh_a, sh_b = shh[i], shh[i + 1]
        if sh_a == 'CCA' and sh_b.startswith('CC'):
            new_forms[i] = f'{new_forms[i]}{x4}'
        elif sh_a.endswith('CC'):
            new_forms[i] = f'{new_forms[i]}{x2}'

    new_lujvo = delim.join(new_forms)
    suffix = f'{x3}a' if new_lujvo[-1] in inv.A else 'a'
    new_lujvo = f'{delim.join(new_lujvo)}{suffix}'
    return new_lujvo

def main(noisy=1): 

    df_lensisku = Table('dictionary-en', 'data/lensisku', keep_default_na=False, sep='\t').dff
    df_lensisku = df_lensisku[df_lensisku['type'] == 'lujvo']

    if noisy:   print('Translating lujvo')
    df_lensisku['word_new'] = df_lensisku['word'].apply(translate_lujvo)

    df_lensisku = df_lensisku[['word', 'word_new', 'glossword_1', 'definition']]
    df_lensisku.to_csv('results/lujvo_new.tsv', sep='\t', index=False)
    return df_lensisku
