# Turns digit-based positional sequences into categorical ones coded for letter types

dcc = ('C1', 'C2', 'A1', 'C3', 'A2')
dca = ('C1', 'A1', 'C2', 'C3', 'A2')
dcc = dict(zip('12345', dcc))
dca = dict(zip('12345', dca))

def pos_to_lpos(s, gismu_type):

    if gismu_type in ('CC', 'CCACA'):
        d = dcc
    elif gismu_type in ('CA', 'CACCA'):
        d = dca
    
    return ''.join(d.get(char, 'XX') for char in s)

    

