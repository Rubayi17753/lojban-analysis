from src.lojban_specific.word_shape import word_shape
from src.utils import rearrange

dcc = ('C1', 'C2', 'A1', 'C3', 'A2')
dca = ('C1', 'A1', 'C2', 'C3', 'A2')
dcc = dict(zip(dcc, '12345'))
dca = dict(zip(dca, '12345'))

def lpos_to_pos(lpos, gismu_type, *args, **kwargs):

    # lpos format: 'CAC 112'
    classes, numbers, *_ = lpos.split(' ')
    lpos = zip(classes, numbers)

    if gismu_type in ('CA', 'CACCA'):
        pos_dict = dca
    elif gismu_type in ('CC', 'CCACA'):
        pos_dict = dcc

    pos = ''.join((pos_dict.get(f'{x}{n}', '__') for (x, n) in lpos))
    return pos

def rearrange_by_lpos(gismu, lpos, reckon=1, gismu_type=None, *args, **kwargs):
    
    if not gismu_type:
        gismu_type = word_shape(gismu)

    pos = lpos_to_pos(lpos, gismu_type)
    form = rearrange(gismu, pos, reckon=reckon)

    return form
    

