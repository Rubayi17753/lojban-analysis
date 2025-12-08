import math
import utils
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

class Out:

    def __init__(self, caa, cca, cac, ccaa, ccac, ccac, cacc):
        self.caa = ''
        self.cca = ''


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

    if row.gismu_type == 'CC':
        out['ccac'] = row.gismu[:4]
    elif row.gismu_type == 'CA':
        out['cacc'] = row.gismu[:4]

    # form_shape = CAA
    if row.params1 == ('CA', '125'):
        ...
    elif row.params1 in (('CC', '135'), ('CC', '235')):
        out['caa'] = row.form

    # form_shape = CAC
    elif row.params1 in (('CA', '123'), ('CA', '124')):
        out['cac'], out['caac'] = row.form, utils.rearrange(row.gismu, '135')
    elif row.params1 == (('CC', '134'), ('CC', '132')):
        out['cac'], out['caac'] = row.form, utils.rearrange(row.gismu, '125')

    # form_shape = CCA
    elif row.params1 == ('CA', '132'):
        out['cca'] = row.form
    elif row.params1 == ('CA', '345'):
        out['cca'] = row.form
    elif row.params1 == ('CC', '123'):
        a, b = row.form, row.gismu
        out['cca'], out['ccaa'], out['ccac'] = a, f'{a}{b[4]}' , a[:4]
    elif row.params1 == ('CC', '345'):

    return out

        



