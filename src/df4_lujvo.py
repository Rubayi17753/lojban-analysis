import pandas as pd
from src.classes.table import Table
import src.lojban_specific.phonological_inventory as inv
import config.hyphens as hyphens
import config.misc as misc_config
from src.lojban_specific.word_shape import word_shape
from src.lojban_specific.parser import lujvo_parser, determine_wordclass
from src.df_gismu_rafsi import get_df_gismu_rafsi
from src.lojban_specific.obtain_specific_cmavo import rafsi_list
import src.newlang_specific.sound_changes as sound_changes


# df = Table('new_gismu', 'interactive', keep_default_na=False, sep=misc_config.new_gismu['sep']).dff
# dict_stem = dict(zip(df['gismu'], df['current_stem']))

df = Table('summary', 'results', keep_default_na=False, sep=misc_config.new_gismu['sep']).dff
dict_stem = dict(zip(df['gismu'], df['current_stem']))
df['current_combining'] = df['current_stem'].apply(sound_changes.stem_to_combining)
df['current_lemma'] = df['current_stem'].apply(sound_changes.stem_to_lemma)
df['current_lemma_count'] = df.groupby('current_lemma')['gismu'].transform('count')

dict_combining = dict(zip(df['gismu'], df['current_combining']))
dict_lemma = dict(zip(df['gismu'], df['current_lemma']))

# df_rafsi_to_gismu = Table('defs_rafsi', keep_default_na=False, sep=',').dff[['rafsi', 'gismu']]
df_rafsi_to_gismu = get_df_gismu_rafsi()
dict_rafsi_to_gismu = dict(zip(df_rafsi_to_gismu['rafsi'], df_rafsi_to_gismu['gismu']))

# rafsi_se_nu = rafsi_list('SE') + rafsi_list('NU')
rafsi_se_nu = [
    'dum', 'jez', 'kam', 'liz', 'muf', 'nil', 'nun', 'puv', 'siz', 'suv', 'zaz', 'zum',
    'sel', 'ter', 'vel', 'xel',
    ]
rafsi_se_nu_new = [
    'du-', 'jeu-', 'ka-', 'li-', 'mu-', 'ni-', 'nu-', 'pu-', 'si-', 'su-', 'zai-', 'zu-',
    'se-', 'te-', 've-', 'xe-',
    ]
dict_switch = dict(zip(rafsi_se_nu, rafsi_se_nu_new))

def _translate_lujvo(lujvo, undetected_rafsi, dict_cmavo, delim=''):

    def rafsi_to_gismu(s):
        s2 = dict_rafsi_to_gismu.get(s, s)

        if not s2:
            undetected_rafsi[s] = undetected_rafsi.get(s, 0) + 1

        elif s in rafsi_se_nu:
            s2 = dict_switch.get(s, s)

        elif len(s2) < 5:
            dict_cmavo[s] = dict_cmavo.get(s, 0) + 1
            s2 = f'{s2}{hyphens.cmavo}'

        return s2

    def gismus_to_word(rafsis):
        gismus = [rafsi_to_gismu(raf) for raf in rafsis]
        
        new_forms = [dict_combining.get(gis, gis) for gis in gismus[:-1]]
        new_forms.append(dict_lemma.get(gismus[-1], f'{gismus[-1]}{hyphens.lemma}'))

        for i, (gismu, new_form) in enumerate(zip(gismus, new_forms)):
            if not new_form:
                new_forms[i] = f'[[{gismu}]]'

        new_lujvo = delim.join(new_forms)
        return new_lujvo

    def switch_se_nu(rafsis):
        len_rafsis = len(rafsis)
        switch_poss = list()    # positions of rafsi to be switched

        for i, (raf,) in enumerate(zip(rafsis,)):
            if raf in rafsi_se_nu and i < len_rafsis:
                switch_poss.append(i)
                
        if switch_poss:
            for pos in switch_poss:
                rafsis[pos], rafsis[pos + 1] = rafsis[pos + 1], rafsis[pos]

        return rafsis

    rafsis = switch_se_nu(rafsis)
    rafsis = lujvo_parser(lujvo, noisy=1)
    new_lujvo = gismus_to_word(rafsis)

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

    # print_undetected_rafsi(undetected_rafsi)
    print_data_cmavo(dict_cmavo)

    df_lensisku = df_lensisku[['word', 'word_new', 'glossword_1', 'definition']]
    df_lensisku.to_csv('results/lensisku_new.tsv', sep='\t', index=False)
    return df_lensisku
