import pandas as pd
from src.classes.table import Table
import src.lojban_specific.phonological_inventory as inv
from src.lojban_specific.word_shape import word_shape
from src.lojban_specific.parser import lujvo_parser, determine_wordclass
from src.df_gismu_rafsi import get_df_gismu_rafsi
import src.newlang_specific.hyphens as hyphens

df_new_gismu = Table('new_gismu', 'interactive', keep_default_na=False, sep='\t').dff
dict_stem = dict(zip(df_new_gismu['gismu'], df_new_gismu['current_stem']))
dict_combining = dict(zip(df_new_gismu['gismu'], df_new_gismu['current_combining']))
dict_lemma = dict(zip(df_new_gismu['gismu'], df_new_gismu['current_lemma']))

# df_rafsi_to_gismu = Table('defs_rafsi', keep_default_na=False, sep=',').dff[['rafsi', 'gismu']]
df_rafsi_to_gismu = get_df_gismu_rafsi()
dict_rafsi_to_gismu = dict(zip(df_rafsi_to_gismu['rafsi'], df_rafsi_to_gismu['gismu']))

def translate_lujvo(lujvo, delim=''):

    def rafsi_to_gismu(s):
        s = dict_rafsi_to_gismu.get(s, f'[{s}]')

        if len(s) < 5:
            s = f'{s}{hyphens.cmavo}'

        return s

    rafsis = lujvo_parser(lujvo, noisy=1)
    gismus = [rafsi_to_gismu(raf) for raf in rafsis]
    new_forms = [dict_combining.get(gis, gis) for gis in gismus[:-1]]
    new_forms.append(dict_lemma.get(gismus[-1], gismus[-1]))

    new_lujvo = delim.join(new_forms)
    return new_lujvo

def main(noisy=1): 

    df_lensisku = Table('dictionary-en', 'data/lensisku', keep_default_na=False, sep='\t').dff
    df_lensisku = df_lensisku[df_lensisku['type'] == 'lujvo']

    if noisy:   print('Translating lujvo')
    df_lensisku['word_new'] = df_lensisku['word'].apply(translate_lujvo)

    df_lensisku = df_lensisku[['word', 'word_new', 'glossword_1', 'definition']]
    df_lensisku.to_csv('results/lujvo_new.tsv', sep='\t', index=False)
    return df_lensisku
