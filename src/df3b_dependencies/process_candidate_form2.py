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
            
            x = d['cmavo_rafsi_1'], d['form_shape_1'], d['rafsi_pos_1']
            y = d['cmavo_rafsi_2'], d['form_shape_2'], d['rafsi_pos_2']

            if (coef_second_form > th.coef_flip_threshhold
                and d['form_shape_1'] == 'CAA' and d['form_shape_2'] != 'CAA'):
                self.form1, self.shape1, self.pos1 = y
                self.form2, self.shape2, self.pos2 = x
            else:
                self.form1, self.shape1, self.pos1 = x
                self.form2, self.shape2, self.pos2 = y

            self.form1 = self.form1.replace("'", '')
            self.form2 = self.form2.replace("'", '')

            if not self.form1:
                self.pos_tendency = 'neut'
            
            self.gismu_type = self.gismu_shape[:2]

            # Normalise pos
            pos_dict = {'132': '134',
                    '231': '234',
                    '342': '345', '145': '345', '142': '345',
                    }
            self.pos1 = pos_dict.get(self.pos1, self.pos1)
            self.pos2 = pos_dict.get(self.pos2, self.pos2)

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
        return ( d['cmavo_rafsi_1'], d['cmavo_rafsi_2'], d['cmavo_rafsi_3'], 
        *d['excluded_a'].split(' '), 
        *d['excluded_b'].split(' ') )

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

def stage1(d):

    out = list()
    row = Row(d)

    cand1 = apply_sound_changes(row.form1)

def process_candidates(df):
    ...


