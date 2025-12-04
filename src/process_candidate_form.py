import math

diphthong_conversion = {
    "a'a" : "a",
    "a'e" : "ai",
    "a'i" : "ai",
    "ai" : "ai",
    "a'o" : "au",
    "a'u" : "au",
    "au" : "au",
    "e'e" : "e",
    "e'i" : "e",
    "ei" : "e",
    "e'o" : "eu",
    "e'u" : "eu",
    "i'e" : "i",
    "i'i" : "i",
    "e'a" : "ia",
    "i'a" : "ia",
    "i'o" : "iu",
    "i'u" : "iu",
    "o'o" : "o",
    "o'u" : "o",
    "o'e" : "oi",
    "o'i" : "oi",
    "oi" : "oi",
    "u'o" : "u",
    "u'u" : "u",
    "o'a" : "ua",
    "u'a" : "ua",
    "u'e" : "ui",
    "u'i" : "ui",
}

coda_conversion = dict(zip('bpfvdtgkxcjszlmnr', 'bbbbddgggsssslmnr'))

def process_candidate_form(row):

    form = row['cmavo_rafsi_1']
    shape = row['form_shape_1']
    pos = row['rafsi_pos_1']
    gismu = row['gismu']
    gismu_shape = row['gismu_shape']
    pos_tendency = row['pos_tendency']  

    # Process forms

    if not form: 
        form = gismu[:4]

    elif shape == 'CAC':
        a = form[:2]
        b = form[2]
        b2 = coda_conversion.get(b, b)
        form = f'{a}{b2}'

    elif 'AA' in shape:
        # CA(')A CCA(')A CCA(')AC
        n = 2 if shape[1] == 'C' else 1     # 2 if CC-, 1 if C-
        p = -1 if shape[-1] == 'C' else 0   # -1 if -C (ends in consonant), else 0

        if shape[1] == 'C':
            a, b, c = form[:2], form[2:-1], form[-1]
        else:
            a, b, c = form[:1], form[1:], ''

        b2 = diphthong_conversion.get(b, b)

        if len(b2) == 2:
            if gismu_shape == 'CCACA' and pos_tendency != 'fin':
                form = f'{gismu[:2]}{b2}{c}'
            else:
                form = f'{a}{b2}{c}'
        
        elif len(b2) == 1:

            forms_secondary = {row['cmavo_rafsi_2'], row['cmavo_rafsi_3']}
            excluded_forms = row['excluded']
            if excluded_forms:
                forms_secondary.update(excluded_forms.split(' '))

            if gismu[:3] in excluded_forms:
                print(f'{gismu[:3]} {excluded_forms}')
                form = gismu[:3]    # 123
            else:
                form = f'{a}{b2}{gismu[3]}'    # 124
            shape = 'CAC'

    if shape.startswith('CC'):
        # CCA, CCAC: xl > kl, xr > kr
        if form[0] == 'h':
            b = form[1:]
            form = f'k{b}'

    return form


    