import math
import pandas as pd
import src.utils as utils
import src.newlang_specific.sound_changes as sound_changes
import src.newlang_specific.phonology as phon

cols = ('ca', 'caa', 'cca', 'cac', 'caac', 'cacc', 'ccaa', 'ccac')
len_cols = tuple(len(col) for col in cols)

class Row:

    def __init__(self, d: dict):
        self.rowdata = d
        self.form = d['cmavo_rafsi_1'].replace("'", "")
        self.form_shape = d['form_shape_1']
        self.pos = d['rafsi_pos_1']
        self.gismu = d['gismu']
        self.gismu_shape = d['gismu_shape']
        self.pos_tendency = d['pos_tendency']

        self.gismu_type = self.gismu_shape[:2]

    @property
    def params1(self):
        return (self.gismu_type, self.pos)

    def c1c2(self):
        cc = ''
        g = self.gismu
        if self.gismu_type == 'CC':    cc =  g[:2]
        elif self.gismu_type == 'CA':    cc = f'{g[0]}{g[2]}'
        return cc

    def diphthong_reduced(self):
        aa = ''
        g = self.gismu
        if self.gismu_type == 'CC':    aa =  f'{g[2]}{g[4]}'
        elif self.gismu_type == 'CA':    aa = f'{g[1]}{g[4]}'
        return (1 if aa in phon.reduced_diphthongs else 0)

    def get_other_rafsi(self):
        d = self.rowdata
        return ( d['cmavo_rafsi_2'], d['cmavo_rafsi_3'], *d['excluded'].split(' ') )

    def find_in_shape(s):
        if s in gismu_shape:
            return gismu_shape.index(s)
        else:
            return -1

def metathesis():
    # check if C1 and C2 allows metathesis
    aa = f'{gismu[0]}{gismu[2]}'
    if aa in phon.valid_cons_pairs:
        form, shape = f'{aa}{b2}{c}', 'CCAA'

def caa_to_cac(out, row):
    # Investigate other rafsi
    cac = None
    g = row.gismu
    for iii in ('123', '124'): 
        threeletter = utils.rearrange(g, iii)
        if threeletter in row.get_other_rafsi():
            cac = threeletter
    if not cac:
        cac = f'{g[:2]}_'
    return cac

def stage1(d):

    row = Row(d)
    out = {col: None for col in cols}
    f, g = row.form, row.gismu

    if row.gismu_type == 'CC':
        out['ccac'] = g[:4]
    elif row.gismu_type == 'CA':
        out['cacc'] = g[:4]

    if row.form_shape == 'CA':
        out['ca'] = f

    if row.form_shape == 'CAA':
        out['caa'] = f
        if row.params1 == ('CA', '125'):
            out['caac'] = utils.rearrange(g, '1254')
            out['ccaa'] = utils.rearrange(g, '1325') 
        elif row.params1 in (('CC', '135'), ('CC', '235')):
            ic = row.pos[0]
            out['caac'], out['ccaa'] = utils.rearrange(g, f'{ic}354'), utils.rearrange(g, '1235')     

    if row.form_shape == 'CAC':
        out['cac'] = f
        if row.params1 in (('CA', '123'), ('CA', '124')):
            fc = row.pos[-1]
            out['caac'] = utils.rearrange(g, f'125{fc}')
        elif row.params1 in (('CC', '134'), ('CC', '132'), ('CC', '234'), ('CC', '231'),):
            ic = row.pos[0]
            out['caac'] = utils.rearrange(g, f'{ic}354') 
    
    if row.form_shape == 'CCA':
        out['cca'] = f
        if row.params1 == ('CA', '132'):
            out['ccac'] = f'{f}{g[3]}'
        elif row.params1 == ('CC', '123'):
            pass
        if row.params1 in (('CA', '132'), ('CC', '123')):
            out['ccaa'] = f'{f}{g[4]}'

    out = apply_sound_changes_to_row(out)
    out = stage1c(out, row)

    return out

def apply_sound_changes_to_row(out):
    
    for col in cols:
        
        v = out[col]
        p, q, r = v, '', ''

        if v:
            if col in ('cca', 'ccaa'):
                if v[:2] in phon.valid_cons_pairs:
                    p, q, r = v[:2], v[2:], ''
                else:
                    p = ''
            elif col == 'ccac':
                p, q, r = v[:2], v[2], v[3]
            elif col == 'cac':
                p, q, r = v[0], v[1], v[2]
            elif col == 'caa':
                p, q, r = v[0], v[1:], ''
            elif col == 'caac':
                p, q, r = v[0], v[1:3], v[3]
            elif col == 'cacc':
                p, q, r = v[0], v[1], v[2:]

            p = sound_changes.clusters_ini.get(p, p) 
            q = sound_changes.diphthongs.get(q, q)
            r = sound_changes.clusters_fin.get(r, r)            
            out[col] = f'{p}{q}{r}'

    return out

def stage1c(out, row):

    for col, len_col in zip(cols, len_cols):

        v = out[col]
        if v:
            if len(v) != len_col:

                if col == 'caa':
                    if row.gismu_type == 'CA':
                        out['cac'] = caa_to_cac(out, row)
                    elif row.gismu_type == 'CC':
                        out['cca'] = out.get('cca', v)
                elif col == 'caac':
                    out['cac'] = out.get('cac', v)
                elif col == 'ccaa':
                    out['cca'] = out.get('cca', v)
            out[col] = None
    return out

def apply_sound_changes_to_df(df):
    # 'ca', 'caa', 'cca', 'cac', 'caac', 'cacc', 'ccaa', 'ccac'
    for col in cols:
        col2 = f'{col}_temp'
        df[col2] = df[col]

    for col in cols:
        col2 = f'{col}_temp'

        if col.startswith('cc'):
            mask = ~(df[col2].str.slice(0, 2).isin(phon.valid_cons_pairs))
            df[col2][mask] = ''
            df[col2] = df[col2].str.slice(0, 2).map(sound_changes.clusters_ini) + df[col2].str.slice(2)

        if col.endswith('aa'):
            df[col2] = df[col2].str.slice(0, -2) + df[col2].str.slice(-2).map(sound_changes.diphthongs)

        if col.endswith('ac'):
            if col.endswith('aac'):
                df[col2] = (df[col2].str.slice(0, -3) 
                            + df[col2].str.slice(-3, -1).map(sound_changes.diphthongs)
                            + df[col2].str[-1].map(sound_changes.cons_coda))
            else:
                df[col2] = df[col2].str.slice(0, -1) + df[col2].str[-1].map(sound_changes.cons_coda)

        if col.endswith('cc'):
            df[col2] = df[col2].str.slice(0, -2) + df[col2].str.slice(-2).map(sound_changes.clusters_fin)

        if col2 in df.columns:
            mask = ~(df[col2].isna())
            df[col2][mask] = df[col2][mask]
        
        df = df.fillna('')

    return df[list(cols)]



