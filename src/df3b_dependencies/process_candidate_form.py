import math
import pandas as pd
import config.misc as config_misc
import config.threshholds as th
import src.utils as utils
import src.lojban_specific.lpos as lpos
import src.lojban_specific.word_shape as word_shape
import src.newlang_specific.sound_changes as sound_changes
import src.newlang_specific.phonology as phon

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

def _get_cac(row, g, ca, n=2):
    coda = row.get_other_coda()
    if not coda:
        coda = g[n] if row.gismu_type == 'CA' else g[3]
    cand = f'{ca}{coda}'
    return cand

def _modify_cac(cand, pos):

    coda = cand[-1]

    dict1 = {'c' : 't', 'b' : 'm'}      # nanca > natca
    dict2 = {'c' : 's', 'b' : 'p'}      # nacna > nasta

    if pos == '124':
        ...

    else:
        ...

    return cand

def stage1(row):
    
    g = row.gismu
    aa = row.diphthong_reduced

    override = row.override
    if override:
        cand = override
    
    elif not row.shape1:
        # i.e. no common rafsi
        cand = row.gismu[:4]
    
    elif row.shape1 == 'CAA' and len(aa) == 1:
        
        if row.form2:
            if row.form1[0] == row.form2[0]:
                cand = row.form2
            else:
                # print(f'{row.form1} {row.form2}')
                cand = row.form2
            
            if row.shape2 == 'CAC':
                cand = _modify_cac(cand, row.pos2)

        else:

            ca = apply_sound_changes(row.form1)
            cc = row.c1c2()

            if len(ca) == 2 and row.pos_tendency == 'ini':  
                if cc in phon.valid_cons_pairs:
                    cand = f'{cc}{ca[1]}'
                    # print(f'{row.form1} {row.form2} {cand}')  
                else:
                    cand = _get_cac(row, g, ca)
            else:
                cand = _get_cac(row, g, ca)
    
    else:
        cand = row.form1
        if row.shape2 == 'CAC':
            cand = _modify_cac(cand, row.pos1)

    cand = apply_sound_changes(cand)
    
    # if row.shape1 == 'CAC' and g[2:4] in sound_changes.coda_stem_to_lemma.values():
    #    cand = f'{row.form1}_'
    
    return cand

def _stage1b(row, c, sh, prev, ri, rf, rcoef2, osf):

    cand = ''
    if sh[-1] == '_':
        cand = f'{row.c1c2}{prev[1]}'

    cand = apply_sound_changes(cand)
    return cand 

def stage2a(row, c, sh, prev, ri, rf, rcoef2, osf):

    g = row.gismu
    cand = ''

    if c > 1 and not row.override and sh == 'CAA':
        ca = prev[0:2]
        cand = f'{ca}{g[3]}'

    cand = apply_sound_changes(cand)
    return cand

def stage2aa(row, c, sh, prev, ri, rf, rcoef2, osf):

    g = row.gismu
    ca = apply_sound_changes(row.form1)
    cc = lpos.rearrange_by_lpos(g, 'CC 13')
    cand = ''

    if c > 1 and not row.override:
        if len(ca) == 2:    #  and row.pos_tendency == 'ini'
            cand = _get_cac(row, g, ca, n=3)


    cand = apply_sound_changes(cand)
    return cand

def stage2ab(row, c, sh, prev, ri, rf, rcoef2, osf):

    g = row.gismu
    ca = apply_sound_changes(row.form1)
    cc = lpos.rearrange_by_lpos(g, 'CC 13')
    cand = ''

    if c > 1 and not row.override:
        if len(ca) == 2:
            cand = f'{cc}{ca[1]}'

    cand = apply_sound_changes(cand)
    return cand

def stage2b(row, c, sh, prev, ri, rf, rcoef2, osf):

    cand = ''
    if c > 1 and not row.override and row.coef2 > th.coef_flip_threshhold:
        if row.shape2:
            if row.shape2 == 'CAA':
                aa = row.diphthong_reduced
                if len(aa) > 1:
                    cand = row.form2
            elif row.shape2 in ('CAC', 'CCA'):
                cand = row.form2

    cand = apply_sound_changes(cand)
    return cand

def stage2c(row, c, sh, prev, ri, rf, rcoef2, osf):

    g = row.gismu
    cand = ''
    if c > 1 and not row.override:
        if row.shape1 == 'CAC':
            cac = row.form1
            cand = f'{cac[0:2]}{sound_changes.cons_coda_cac2.get(cac[2], cac[2])}'
    
    cand = apply_sound_changes(cand)
    return cand

def _get_ccaa(row, c, sh, prev, ri, rf, rcoef2, osf, n=2):
    g = row.gismu
    cand = ''
    ca = apply_sound_changes(row.form1)
    if len(ca) == 3:    
        # ca of shape CAA
        if row.pos1 != '345':   #  and row._ri < 30
            cand = lpos.rearrange_by_lpos(g, f'CCAA 1{n}12')
            if cand[:2] not in phon.valid_cons_pairs:
                if row.shape1 in ('CAA', 'CCA'):
                    cand = lpos.rearrange_by_lpos(g, 'CCAA 1312')
    else:
        pass
        # print(ca)
        # ca of shape CA
        # cand = f"{prev[0]}{lpos.rearrange_by_lpos(g, 'C 2')}{prev[1:3]}"  
    return cand 

def stage_ccaa1(row, c, sh, prev, ri, rf, rcoef2, osf):
    cand = ''
    if c > 1 and not row.override and not osf: # and row._rf > 3 #  and row.pos_tendency != 'fin'
        if (row.shape1 in ('CAA', 'CCA')
            or (row.shape1 == 'CAC' and row.pos1 == '123')):
            cand = _get_ccaa(row, c, sh, prev, ri, rf, rcoef2, osf, n=2)
    cand = apply_sound_changes(cand)
    return cand  

def stage_ccaa2(row, c, sh, prev, ri, rf, rcoef2, osf):
    cand = ''
    if c > 1 and not row.override and not osf:  #  and row.pos_tendency != 'fin'
        if (row.shape1 in ('CAA', 'CCA')
            or (row.shape1 == 'CAC' and row.pos1 == '123')):
            cand = _get_ccaa(row, c, sh, prev, ri, rf, rcoef2, osf, n=3)
    cand = apply_sound_changes(cand)
    return cand  

def stage_ccaa3(row, c, sh, prev, ri, rf, rcoef2, osf):
    cand = ''
    if c > 1 and not row.override and not osf:  #  and row.pos_tendency != 'fin'
        if row.shape1 in ('CAA', ):
            cand = _get_ccaa(row, c, sh, prev, ri, rf, rcoef2, osf)
    cand = apply_sound_changes(cand)
    return cand   

def _stage_ccac(row, c, sh, prev, ri, rf, rcoef2, osf, cond):
     
    g = row.gismu
    cand = ''

    # freq_prefix and freq_suffix represent raw rafsi word counts. 
    # They may thus be used to gauge the most frequently-occuring 
    # de-facto 'prefixes' and 'suffixes' in the language.
 
    if c > 1 and not row.override and not osf and cond:  #  and row.pos_tendency != 'fin'
 
        if sh == 'CAC':
            if row.pos1 != '123':   # in ('124', '134', '234')
                cand = lpos.rearrange_by_lpos(g, 'CCAC 1213')
            elif row.pos1 in ('123',):
                cand = lpos.rearrange_by_lpos(g, 'CCAC 1212')   # 1312
        elif sh == 'CCA' and row.pos1 != '345':
            cand = f'{prev}{g[3]}'
    
    cand = apply_sound_changes(cand)
    return cand

def stage_ccac1(row, c, sh, prev, ri, rf, rcoef2, osf):
    return _stage_ccac(row, c, sh, prev, ri, rf, rcoef2, osf, (rf < 0.9 or row.freq_suffix < 5))

def stage_ccac2(row, c, sh, prev, ri, rf, rcoef2, osf):
    return _stage_ccac(row, c, sh, prev, ri, rf, rcoef2, osf, (ri > 0.9 or row.freq_prefix < 5))

def stage_ccac3(row, c, sh, prev, ri, rf, rcoef2, osf):
    return _stage_ccac(row, c, sh, prev, ri, rf, rcoef2, osf, 1)

def _stage_caac(row, c, sh, prev, ri, rf, rcoef2, osf, cond):
     
    g = row.gismu
    cand = ''
    if cond:  # i.e. that leans towards ini the most # ri > 0.9      
        if sh == 'CAA':
            coda = row.get_other_coda()
            if not coda:
                coda = g[2] if row.gismu_type == 'CA' else g[3]
            
            aa_dict = {'ae' : 'ai', 
                        'ao': 'au'
                        }
            aa = lpos.rearrange_by_lpos(g, 'AA 12')
            aa = aa_dict.get(aa, aa)
            cand = f"{g[0]}{aa}{coda}"
        elif sh == 'CAC':
            aa = row.diphthong_reduced
            if len(aa) > 1:
                cand = f"{prev[0]}{aa}{row.form1[-1]}"
    cand = apply_sound_changes(cand)
    return cand

def stage_caac1(row, c, sh, prev, ri, rf, rcoef2, osf):
    cond = c > 1 and not row.override and not osf and rcoef2 != 1
    cand = _stage_caac(row, c, sh, prev, ri, rf, rcoef2, osf, cond)
    return cand

def stage_caac2(row, c, sh, prev, ri, rf, rcoef2, osf):
    cond = c > 1 and not row.override and not osf
    cand = _stage_caac(row, c, sh, prev, ri, rf, rcoef2, osf, cond)
    return cand

def stage_cacn(row, c, sh, prev, ri, rf, rcoef2, osf):
    g = row.gismu
    cand = ''   
    if c > 1 and not row.override and not osf:
        if sh == 'CAC' and row.pos1 in ('123',):
            cac = row.form1
            if cac[-1] not in 'mnlr':
                cand = f'{cac}ñ'
    cand = apply_sound_changes(cand)
    return cand

def stage_fin_metathesis(row, c, sh, prev, ri, rf, rcoef2, osf):
    g = row.gismu
    cand = ''
    if c > 1 and not row.override and row.gismu_type == 'CA' and not osf:
        cand = lpos.rearrange_by_lpos(g, 'CCAC 1213')

    cand = apply_sound_changes(cand)
    return cand

def stage_fin(row, c, sh, prev, ri, rf, rcoef2, osf):

    cand = ''
    if c > 1 and not row.override and not osf:
        cand = row.gismu[:4]

    cand = apply_sound_changes(cand)
    return cand

def stage_fin_ccaa(row, c, sh, prev, ri, rf, rcoef2, osf):
    g = row.gismu
    aa = row.diphthong_reduced
    cand = ''
    if not row.override and sh in ('CACC', 'CCAC') and not osf and row._ri > 5:
        if len(aa) == 2:
            cand = lpos.rearrange_by_lpos(g, 'CCAA 1212')

    cand = apply_sound_changes(cand)
    return cand

def stage_fin_metathesis2(row, c, sh, prev, ri, rf, rcoef2, osf):
    g = row.gismu
    cand = ''
    if not row.override and (sh == 'CACC' or (sh == 'CCAA' and c > 1)) and not osf and row._ri > 5:
        cand = lpos.rearrange_by_lpos(g, 'CCAC 1213')

    cand = apply_sound_changes(cand)
    return cand

def stage_alter(row, c, sh, prev, ri, rf, rcoef2, osf):
    g = row.gismu
    cand = ''
    if (sh == 'CCA' 
    and row._ri < 2 and row.pos1 != '345'
    and not row.override and not osf):
        cand = lpos.rearrange_by_lpos(g, 'CCAC 1213')

    cand = apply_sound_changes(cand)
    return cand

def identify_unique(row, c, sh, prev, ri, rf, rcoef2, osf):

    cand = ''
    if row.form1 and row.form2:
        if row.form1[0] != row.form2[0]:
            to_print = [row.gismu, row.form1, row.form2, row.shape1, row.shape2]
            print('\t'.join(to_print))
    return cand

stage_data = {
    stage1 : None,
    stage2a : None, 
    stage2aa : None, 
    stage2ab : None,   
    stage2b : None,
    stage2c : None, # {'purge_forms_already_used': 0}
    stage_ccaa1 : None,
    # stage_ccaa2 : None,
    stage_ccaa3 : None,
    stage_ccac1 : None,
    stage_ccac2 : None,
    # stage_ccac3 : None,
    stage_caac1: None,
    stage_caac2: None,
    # stage_cacn: None,
    stage_fin_metathesis: None,
    stage_fin: None,
    # stage_fin_ccaa: None,
    stage_fin_metathesis2: None,
    stage_alter: None,
    # identify_unique: None,
}

stages, stages_param = stage_data.keys(), stage_data.values()
