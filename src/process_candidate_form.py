import math
import pandas as pd
import config.threshholds as th
import src.utils as utils
import src.lojban_specific.phonological_inventory as inv
import src.newlang_specific.sound_changes as sound_changes
import src.newlang_specific.phonology as phon

cols = ('override', 'ca', 'caa', 'cca', 'cac', 'caac', 'cacc', 'ccaa', 'ccac')
len_cols = tuple(len(col) for col in cols)
amount_cols = len(cols)

class Row:

    def __init__(self, d: dict):
        self.rowdata = d
        self.override = d['override']
        self.gismu = d['gismu']
        self.gismu_shape = d['gismu_shape']
        self.poss_tendency = d['pos_tendency']

        if self.gismu:

            # Admit second forms if certain criteria met
            # Second before first, so that first forms overwrite second
            n1, n2 = d['coef1_1'], d['coef1_2']

            coef_second_form = round(n2 / n1 , 1) if n1 else 999
            
            if coef_second_form > th.coef_second_form_threshhold:
                self.forms = [d['cmavo_rafsi_2'] , d['cmavo_rafsi_1']]
                self.shapes = [d['form_shape_2'] , d['form_shape_1']]
                self.poss = [d['rafsi_pos_2'] , d['rafsi_pos_1']]
                self.priority_factors = [1, 1] if coef_second_form > 0.5 else [0.5, 1]
            else:
                self.forms = [d['cmavo_rafsi_1']]
                self.shapes = [d['form_shape_1']]
                self.poss = [d['rafsi_pos_1']]
                self.priority_factors = [1,]
            
            if not self.forms[0]:
                # i.e. self.forms, .shapes, .poss are lists of empty strings
                self.forms = [d['gismu'][:-1]]
                self.shapes = [d['gismu_shape'][:-1]]
                self.poss = ['neut']
                
            self.forms = [x.replace("'", "") for x in self.forms] 

            self.gismu_type = self.gismu_shape[:2]
            self.params = [(self.gismu_type, x) for x in self.poss]         

    @property
    def params1(self):
        return (self.gismu_type, self.poss)

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

    def find_in_shape(s):
        if s in gismu_shape:
            return gismu_shape.index(s)
        else:
            return -1

class Form:

    def __init__(self, form=None, priority=0):
        self.form = form
        self.priority = priority

def stage1(d, ordered=1):

    row = Row(d)
    out = {col: Form() for col in cols}

    out['override'].form = row.override
    out['override'].priority = -1000
    out['ca'].priority = -500

    for form_args in zip(row.forms, row.shapes, row.poss, row.params, row.priority_factors):
        out = process_form(out, row, *form_args)
    out = apply_sound_changes_to_row(out)
    out = stage1c(out, row)

    if ordered:
        out = [v.form for k, v in sorted(out.items(), key = lambda item : item[1].priority)]
        out = tuple(m for m in out if m) # removes blanks and nones
        out = dict(zip( range(amount_cols) , out ))
    else:
        out = {a : b.form for a, b in out.items()}

    return out

def process_form(out, row, *form_args):

    f, fs, pos, params, priority_factor = form_args
    g, gt = row.gismu, row.gismu_type

    if not f:
        print(g)
        return out

    # Boost priority of 'original' form and those that match positional preferences:
    out[fs.lower()].priority += round(-20 * priority_factor)
    
    if pos == 'ini':
        out['cacc'].priority += 20
        for col_coda_c in ('caac', 'ccac'): # cac exempt
            out[col_coda_c].priority += 10

    if pos == 'fin':
        out['ccac'].priority += 20  # cca exempt

    # By gismu shape
    if gt == 'CC':
        out['ccac'].form = g[:4]
    elif gt == 'CA':
        out['cacc'].form = g[:4]

    # By form shape and pos
    if fs == 'CA':
        out['ca'].form = f

    if fs == 'CAA':
        out['caa'].form = f
        if params == ('CA', '125'):
            fc = row.get_other_coda()
            fc = fc if fc else g[3]     # supply last consonant if list of codas empty
            out['caac'].form = f'{f}{fc}'
            out['ccaa'].form = utils.rearrange(g, '1325') 
        elif params in (('CC', '135'), ('CC', '235')):
            ic = pos[0]
            out['caac'].form = utils.rearrange(g, f'{ic}354')
            out['ccaa'].form = utils.rearrange(g, '1235')     

    if fs == 'CAC':
        out['cac'].form = f
        if params in (('CA', '123'), ('CA', '124')):
            fc = pos[-1]
            out['caac'].form = utils.rearrange(g, f'125{fc}')
        elif params in (('CC', '134'), ('CC', '132'), ('CC', '234'), ('CC', '231'),):
            ic = pos[0]
            out['caac'].form = utils.rearrange(g, f'{ic}354') 
        if params == ('CA', '124'):
            out['ccac'].form = utils.rearrange(g, f'1324')
    
    if fs == 'CCA':
        out['cca'].form = f
        if params == ('CA', '132'):
            out['ccac'].form = f'{f}{g[3]}'
        if params in (('CA', '132'), ('CC', '123')):
            out['ccaa'].form = f'{f}{g[4]}'

    return out

def apply_sound_changes_to_row(out):
    
    for col in cols:
        
        v = out[col].form
        p, q, r = v, '', ''

        if v:
            if col in ('cca', 'ccaa', 'ccac'):
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
            out[col].form = f'{p}{q}{r}'

    return out

def stage1c(out, row):

    for col, len_col in zip(cols, len_cols):

        # print(list(x.form for x in out.values()))

        vv = out[col]
        v = vv.form
        g = row.gismu

        if v and col != 'override':
            if len(v) != len_col:
                if col == 'caa':
                    if row.gismu_type == 'CA':
                        fc = row.get_other_coda()
                        fc = fc if fc else '_'     # supply '_' if list of codas empty
                        out['cac'].form = f'{v}{fc}'    # CA +
                    elif row.gismu_type == 'CC':
                        out['cac'].form = f'{v}{g[3]}'    # CA + A
                        out['cca'].form = f'{g[:2]}{v[-1]}'     # CC + A
                elif col == 'caac':
                    out['cac'].form = out.get('cac', vv).form
                elif col == 'ccaa':
                    out['cca'].form = out.get('cca', vv).form
                out[col].form = None

    return out


