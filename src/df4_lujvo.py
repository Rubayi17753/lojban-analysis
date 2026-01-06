import pandas as pd
from src.classes.table import Table
import src.lojban_specific.phonological_inventory as inv
from src.lojban_specific.word_shape import word_shape
from src.lojban_specific.parser import lujvo_parser, determine_wordclass
from src.df_gismu_rafsi import get_df_gismu_rafsi
import config.hyphens as hyphens

df_new_gismu = Table('new_gismu', 'interactive', keep_default_na=False, sep='\t').dff
dict_stem = dict(zip(df_new_gismu['gismu'], df_new_gismu['current_stem']))
dict_combining = dict(zip(df_new_gismu['gismu'], df_new_gismu['current_combining']))
dict_lemma = dict(zip(df_new_gismu['gismu'], df_new_gismu['current_lemma']))

# df_rafsi_to_gismu = Table('defs_rafsi', keep_default_na=False, sep=',').dff[['rafsi', 'gismu']]
df_rafsi_to_gismu = get_df_gismu_rafsi()
dict_rafsi_to_gismu = dict(zip(df_rafsi_to_gismu['rafsi'], df_rafsi_to_gismu['gismu']))

def _translate_lujvo(lujvo, undetected_rafsi, dict_cmavo, delim=''):

    def rafsi_to_gismu(s):
        s2 = dict_rafsi_to_gismu.get(s, '')

        if not s2:
            undetected_rafsi[s] = undetected_rafsi.get(s, 0) + 1

        elif len(s2) < 5:
            dict_cmavo[s] = dict_cmavo.get(s, 0) + 1
            s2 = f'{s2}{hyphens.cmavo}'

        return s2

    rafsis = lujvo_parser(lujvo, noisy=1)
    gismus = [rafsi_to_gismu(raf) for raf in rafsis]
    new_forms = [dict_combining.get(gis, gis) for gis in gismus[:-1]]
    new_forms.append(dict_lemma.get(gismus[-1], gismus[-1]))

    new_lujvo = delim.join(new_forms)
    return new_lujvo

def main(noisy=1): 

    undetected_rafsi = dict()
    dict_cmavo = dict()

    df_lensisku = Table('dictionary-en', 'data/lensisku', keep_default_na=False, sep='\t').dff
    df_lensisku = df_lensisku[df_lensisku['type'] == 'lujvo']

    def translate_lujvo(lujvo):
        return _translate_lujvo(lujvo, undetected_rafsi, dict_cmavo)

    if noisy:   print('Translating lujvo')
    df_lensisku['word_new'] = df_lensisku['word'].apply(translate_lujvo)

    def print_undetected_rafsi(undetected_rafsi):
        undetected_rafsi = [{'rafsi': k, 'form_len': len(k), 'form_count': v} 
                            for k, v in undetected_rafsi.items()]
        df_undetected_rafsi = pd.DataFrame(undetected_rafsi)
        df_undetected_rafsi = df_undetected_rafsi.sort_values(
                by=['form_len', 'form_count'],
                ascending=[True, False]
            )
        df_undetected_rafsi.to_csv('results/lensisku_undetected_forms.tsv', sep='\t', index=False)

    def print_data_cmavo(dict_cmavo):
        dict_cmavo = [{'rafsi': k, 'cmavo': dict_rafsi_to_gismu.get(k, ''), 'form_count': v} 
                            for k, v in dict_cmavo.items()]
        df_dict_cmavo = pd.DataFrame(dict_cmavo)
        df_dict_cmavo = df_dict_cmavo.sort_values(
                by=['form_count', ],
                ascending=[False, ]
            )
        df_dict_cmavo.to_csv('results/lensisku_dict_cmavo.tsv', sep='\t', index=False)

    print_undetected_rafsi(undetected_rafsi)
    print_data_cmavo(dict_cmavo)

    df_lensisku = df_lensisku[['word', 'word_new', 'glossword_1', 'definition']]
    df_lensisku.to_csv('results/lensisku_new.tsv', sep='\t', index=False)
    return df_lensisku
