import math
import src.utils as utils
from src.newlang_specific.phonology import valid_cons_pairs

class Row:

    def __init__(self, d: dict):
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

class Out:

    def __init__(self, caa, cca, cac, caac, cacc, ccaa, ccac):
        ...


def metathesis():
    # check if C1 and C2 allows metathesis
    aa = f'{gismu[0]}{gismu[2]}'
    if aa in valid_cons_pairs:
        form, shape = f'{aa}{b2}{c}', 'CCAA'

def stage1(d):

    row = Row(d)
    out = {col: None for col in 
            ('caa', 'cca', 'cac', 'cacc', 'ccaa', 'ccac', 'ccac')
        }
    f, g = row.form, row.gismu

    if row.gismu_type == 'CC':
        out['ccac'] = g[:4]
    elif row.gismu_type == 'CA':
        out['cacc'] = g[:4]

    # form_shape = CAA
    if row.params1 == ('CA', '125'):
        out['caa'], out['caac'] = f, utils.rearrange(g, '1254')
    elif row.params1 == ('CC', '135'):
        out['caa'], out['caac'], out['ccaa'] = f, utils.rearrange(g, '1354'), utils.rearrange(g, '1235')
    elif row.params1 == ('CC', '235'):
        out['caa'], out['caac'], out['ccaa'] = f, utils.rearrange(g, '2354'), utils.rearrange(g, '1235')

    # form_shape = CAC
    elif row.params1 in (('CA', '123'), ('CA', '124')):
        out['cac'], out['caac'] = f, utils.rearrange(g, '1354')
    elif row.params1 == (('CC', '134'), ('CC', '132')):
        out['cac'], out['caac'] = f, utils.rearrange(g, '1354')
    elif row.params1 == (('CC', '234'), ('CC', '231'),):
        out['cac'], out['caac'] = f, utils.rearrange(g, '2354')

    # form_shape = CCA:
    elif row.params1 == ('CA', '132'):
        out['cca'], out['ccaa'], out['ccac'] = f, f'{f}{g[4]}', f'{f}{g[3]}'
    elif row.params1 == (tuple('CC', ii) for ii in ('345', '342', '145', '142')):
        out['cca'], out['ccaa'] = f, f'{f}{g[4]}'
    elif row.params1 == ('CC', '123'):
        out['cca'], out['ccaa'] = f, f'{f}{g[4]}'

    c1c2 = row.c1c2()
    if c1c2:
        if row.params1 in ('CA', '125'):
            out['ccaa'], out['ccac'] = utils.rearrange(g, '1325'), utils.rearrange(g, '1324')
        elif row.params1 in ('CA', '124'):
            out['ccac'] = f'{c1c2}{f[-2:]}'

    return out

        



