import math
import pandas as pd
import config.misc as config_misc
import src.utils as utils
import src.lojban_specific.word_shape as word_shape
import src.newlang_specific.sound_changes as sound_changes
import src.newlang_specific.phonology as phon
import config.hyphens as hyphen

# cols = ('override', 'CA', 'caa', 'cca', 'cac', 'cak', 'coc', 'cok', 'cacc', 'ccaa', 'ccac', 'ccoc')
cols = (
    'form1a', 'form2a', 'CAAC1a', 'CAAC1b', 
    'form1b', 'form1bb', 'form2b', 'form2bb', 'CCAA1', 
    'form4a', 'form1c', 'form2c', 'CAACa', 'CAACb',
    'CCAA2' 
    'form4b'
    )
amount_cols = len(cols)

def get_alt_coda(coda):
    alt_coda = sound_changes.cons_coda_ccac.get(coda, '')
    coda2 = sound_changes.cons_coda_cac.get(coda)
    if alt_coda == coda2:
        alt_coda = ''
    return alt_coda

def unique(lst, default=''):
    # Turns second and subsequent occurrences of items in a list into blank strings 
    holder = set()
    for a in lst:
        ...

def apply_sound_changes(v):
    
    p, q, r = v, '', ''
    
    if v:

        shape = word_shape.word_shape(v)
        if shape == 'CCAC':
            (p, q, r) = (v[:2], v[2], v[3]) if v[:2] in phon.valid_cons_pairs else ('', '', '')
        elif shape in ('CCA', 'CCAA'):
            (p, q, r) = (v[:2], v[2:], '') if v[:2] in phon.valid_cons_pairs else ('', '', '')        
        elif shape == 'CAAC':
            p, q, r = v[0], v[1:3], v[3]        
        elif shape == 'CAC':
            p, q, r = v[0], v[1], v[2]
        elif shape == 'CAA':
            p, q, r = v[0], v[1:], ''
        elif shape == 'CACC':
            p, q, r = v[0], v[1], v[2:]

        if shape == 'CCAC':
            dict_r = sound_changes.cons_coda_ccac
        elif shape == 'CAC':
            dict_r = sound_changes.cons_coda_cac
        elif shape == 'CAAC':
            dict_r = sound_changes.cons_coda_caac
        else:
            dict_r = sound_changes.clusters_fin

        p = sound_changes.clusters_ini.get(p, p) 
        q = sound_changes.diphthongs.get(q, q)
        r = dict_r.get(r, r) 

        if r == '_':
            p, q, r = '', '', ''

        v = f'{p}{q}{r}'

    return v

def stage1(row):
    
    aa = row.diphthong_reduced

    override = row.override
    if override:
        cand = override
    elif not row.shape1:
        # i.e. no common rafsi
        cand = apply_sound_changes(row.gismu[:4])
    elif row.shape1 == 'CAA' and len(aa) == 1:
        if row.form2:
            cand = apply_sound_changes(row.form2)
        else:
            cand = apply_sound_changes(row.form1)
            cand = f'{cand}_'
    else:
        cand = apply_sound_changes(row.form1)

    return cand

def stage2(row, c, sh):

    cand = ''
    if c > 1 and not row.override:
        if sh == 'CAC':
            ...

stages = [stage1, ]

