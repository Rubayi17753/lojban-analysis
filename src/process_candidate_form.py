import math
import pandas as pd
import config.threshholds as th
import config.misc as config_misc
import src.utils as utils
import src.lojban_specific.phonological_inventory as inv
import src.lojban_specific.lpos as lpos
import src.lojban_specific.word_shape as word_shape
import src.newlang_specific.sound_changes as sound_changes
import src.newlang_specific.phonology as phon

# cols = ('override', 'CA', 'caa', 'cca', 'cac', 'cak', 'coc', 'cok', 'cacc', 'ccaa', 'ccac', 'ccoc')
cols = ('form1', 'form2', 'CCAA', 'form4a', 'form4b')
amount_cols = len(cols)

class Row:

    def __init__(self, d: dict):
        self.rowdata = d
        self.override = d['override']
        self.gismu = d['gismu']
        self.gismu_shape = d['gismu_shape']
        self.pos_tendency = d['pos_tendency']

        if self.gismu:

            # Admit second forms if certain criteria met
            n1, n2 = d['coef1_1'], d['coef1_2']
            coef_second_form = round(n2 / n1 , 1) if n1 else 999
            
            self.form1, self.shape1, self.pos1 = d['cmavo_rafsi_1'], d['form_shape_1'], d['rafsi_pos_1']
            self.form2, self.shape2, self.pos2 = '', '', ''
            if coef_second_form > th.coef_second_form_threshhold:
                self.form2, self.shape2, self.pos2 = d['cmavo_rafsi_2'], d['form_shape_2'], d['rafsi_pos_2']
       
            if not self.form1:
                self.pos1 = 'neut'
            
            self.gismu_type = self.gismu_shape[:2]

    @property
    def params1(self):
        return (self.gismu_type, self.poss)

    @property
    def diphthong_reduced(self):
        g = self.gismu
        aa = lpos.rearrange_by_lpos(g, 'AA 12')
        return sound_changes.diphthongs.get(aa, aa)

    def c1c2(self):
        cc = ''
        g = self.gismu
        if self.gismu_type == 'CC':    cc =  g[:2]
        elif self.gismu_type == 'CA':    cc = f'{g[0]}{g[2]}'
        return cc

    def get_other_rafsi(self):
        d = self.rowdata
        return ( d['cmavo_rafsi_1'], d['cmavo_rafsi_2'], d['cmavo_rafsi_3'], *d['excluded'].split(' ') )

    def get_other_coda(self):
        rafsis = tuple((form for form in self.get_other_rafsi() if form))
        codas = tuple((char 
                        for char in (form[-1] for form in rafsis)
                        if char in inv.C
                        ))

        if len(codas) > 1:  print(rafsis)
        coda = codas[0] if codas else None
        return coda

    def find_in_shape(self, s):
        if s in self.gismu_shape:
            return self.gismu_shape.index(s)
        else:
            return -1

def stage1(d):

    row = Row(d)
    out = {col: '' for col in cols}
    sh1 = row.shape1
    g = row.gismu
    tend = row.pos_tendency
    aa = row.diphthong_reduced

    if row.override:
        out['form1'] = row.override
        return out

    if sh1 == 'CA':
        out['form1'] = row.shape1
        return out

    if sh1 in ('CAC', 'CCA'):
        out['form1'] = row.form1
    if sh1 == 'CAA':
        if len(aa) <= 1:
            if tend in ('ini', 'neut'):
                out['form1'] = f'{g[0]}{aa}_'
            else:
                out['form1'] = f'{lpos.rearrange_by_lpos(g, "CC 12")}{aa}'
        else:
            out['form1'] = row.form1

    if sh1 == 'CAA' or (sh1 == 'CCA'):    # and row.form1 != g[:-3]
        if len(aa) > 1:
            out['CCAA'] = lpos.rearrange_by_lpos(g, 'CCAA 1212')

    out['form4a'] = lpos.rearrange_by_lpos(g, 'CCAC 1213')
    out['form4b'] = lpos.rearrange_by_lpos(g, 'CACC 1123')

    if row.gismu_type == 'CC':
         out['form4a'], out['form4b'] = out['form4a'], ''
    elif tend not in ('ini', 'neut') :
        out['form4a'], out['form4b'] = out['form4b'], ''

    out = {k : apply_sound_changes(v) for k, v in out.items()}
    stack = [v for v in out.values() if v][::-1]

    print(stack)
    return stack

def apply_sound_changes(v):
    
    p, q, r = v, '', ''
    
    if v:

        shape = word_shape.word_shape(v)
        if shape == 'CCAC':
            (p, q, r) = (v[:2], v[2], v[3]) if v[:2] in phon.valid_cons_pairs else ('', '', '')
        elif shape in ('CCA', 'CCAA'):
            (p, q, r) = (v[:2], v[2:], '') if v[:2] in phon.valid_cons_pairs else ('', '', '')                
        elif shape == 'CAC':
            p, q, r = v[0], v[1], v[2]
        elif shape == 'CAA':
            p, q, r = v[0], v[1:], ''
        elif shape == 'CACC':
            p, q, r = v[0], v[1], v[2:]

        p = sound_changes.clusters_ini.get(p, p) 
        q = sound_changes.diphthongs.get(q, q)
        r = sound_changes.clusters_fin.get(r, r)            
        v = f'{p}{q}{r}'

    return v



