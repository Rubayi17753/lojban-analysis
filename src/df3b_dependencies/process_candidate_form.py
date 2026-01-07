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
            
            self.form1, self.shape1, self.pos1 = d['cmavo_rafsi_1'], d['form_shape_1'], d['rafsi_pos_1']
            self.form2, self.shape2, self.pos2 = '', '', ''
            if coef_second_form > th.coef_second_form_threshhold:
                self.form2, self.shape2, self.pos2 = d['cmavo_rafsi_2'], d['form_shape_2'], d['rafsi_pos_2']
            
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
    alt_coda = '' if alt_coda == coda else alt_coda   
    return alt_coda

def stage1(d):

    def derive_forms(sh, form, pos, i):

        cc = lpos.rearrange_by_lpos(g, "CC 23") 
        coda = row.get_other_coda()

        if coda:
            coda1, coda2 = coda, cc.replace(coda, '')
        else:
            coda1, coda2 = cc if cc in phon.valid_cons_pairs else cc[::-1]
        if coda1 in phon.caac_coda_restriction: coda1 = ''
        if coda2 in phon.caac_coda_restriction: coda2 = ''
            
        if sh == 'CCA':
            if tend != 'fin' or pos == '345':
                out[f'form{i}a'] = f'{form}{hyphen.ca}'
            if row.gismu_type == 'CC' and g[3] == hyphen.ca: 
                out[f'form{i}a'] = f'{form}{hyphen.ca}'

        if sh == 'CAC':
            out[f'form{i}a'] = form
            p, coda = form[:-1], form[-1]
            alt_coda = get_alt_coda(coda)
            if alt_coda:   out[f'form{i}bb'] = f'{p}{coda}'

        if sh == 'CAA':

            if len(aa) <= 1:
                
                    '''
                    cc = lpos.rearrange_by_lpos(g, "CC 12")
                    if tend == 'ini' and cc in phon.valid_cons_pairs:
                        # CCA
                        cc = lpos.rearrange_by_lpos(g, "CC 12")
                        if cc in phon.valid_cons_pairs:
                            out[f'form{i}a'] = f'{cc}{aa}{hyphen.ca}'
                            if oo:
                                out[f'form{i}b'] = f'{cc}{oo}{hyphen.ca}'
                    else:
                    '''
                
                # CAC
                p = f'{form[0]}{aa}'
                q = f'{form[0]}{g[-1]}' # C + final vowel
                if coda1:   
                    out[f'form{i}a'] = f'{p}{coda1}'
                    out[f'form{i}c'] = f'{q}{coda1}'
                if coda2:   out[f'form{i}b'] = f'{p}{coda2}'
                alt_coda = get_alt_coda(coda1)
                if alt_coda:  out[f'form{i}bb'] = f'{p}{alt_coda}'
             
            else:
                # CAA-n
                if tend in ('ini', 'neut'):
                    out[f'form{i}a'] = f'{form}{hyphen.aa}'

            if coda1:   out[f'form{i}c'] = f'{lpos.rearrange_by_lpos(g, "CA 12")}{coda1}'

        if len(aa) > 1:

            caa = f"{form[0]}{lpos.rearrange_by_lpos(g, 'AA 12')}"

            if tend != 'fin' and (sh == 'CAA' or sh == 'CCA'):    
                # and (sh == 'CAA' or sh == 'CCA')
                # and row.form1 != g[:-3]
                out['CCAA1'] = lpos.rearrange_by_lpos(g, 'CCAA 1212')
            
            if sh in ('CAA', 'CCA', 'CAC'):
                out['CCAA2'] = lpos.rearrange_by_lpos(g, 'CCAA 1212')
            
            if sh == 'CAA':
                x, y = '', ''
                if coda1:  x = f"{caa}{coda1}"  
                if coda2:  y = f"{caa}{coda2}"

                if tend in ('fin',):
                    out['CAAC1a'], out['CAAC1b'] = x, y 
                else:
                    out['CAACa'], out['CAACb'] = x, y
            if sh == 'CAC':
                coda = form[-1]
                alt_coda = get_alt_coda(coda)
                out['CAACa'] = f'{caa}{coda}'
                if alt_coda:  out[f'CAACb'] = f'{p}{alt_coda}'

    row = Row(d)
    out = {col: '' for col in cols}
    form1, form2 = row.form1, row.form2
    sh1, sh2 = row.shape1, row.shape2
    pos1, pos2 = row.pos1, row.pos2
    g = row.gismu
    tend = row.pos_tendency
    aa = row.diphthong_reduced

    if len(aa) <= 1:
        oo = lpos.rearrange_by_lpos(g, 'AA 12').replace(aa, '')

    override = row.override
    if override:
        override_suffix = ''
        sh_override = word_shape.word_shape(override)
        if sh_override.endswith('A'):
            override_suffix = hyphen.ca
        out['form1a'] = f'{override}{override_suffix}'

    elif row.shape1 == 'CA':
        out['form1a'] = form1

    elif row.shape1 == 'CCAC':
        out['form1a'] = form1

    else:
        if sh1:
            derive_forms(sh1, form1, pos1, 1)
        if sh2:
            derive_forms(sh2, form2, pos2, 2)

        if row.gismu_type == 'CC' or sh1 == 'CCA' or tend in ('ini', 'neut'):
            out['form4a'] = f"{lpos.rearrange_by_lpos(g, 'CCA 121')}{g[3]}" # CCAC
        out['form4b'] = lpos.rearrange_by_lpos(g, 'CACC 1123')  # CACC

        if row.gismu_type == 'CC':
            out['form4a'], out['form4b'] = out['form4a'], ''
        # elif tend not in ('ini', 'neut'):
            # out['form4a'], out['form4b'] = '', out['form4b']

    out = {k : apply_sound_changes(v) for k, v in out.items()}
    forms = [v for v in out.values()]   # if v
    out['stack'] = forms[::-1]

    return out

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



