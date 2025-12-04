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
    "i'e" : "e",
    "e'o" : "eu",
    "e'u" : "eu",
    "i'i" : "i",
    "e'a" : "ia",
    "i'a" : "ia",
    "i'o" : "iu",
    "i'u" : "iu",
    "o'o" : "o",
    "o'u" : "o",
    "u'o" : "o",
    "o'e" : "oi",
    "o'i" : "oi",
    "oi" : "oi",
    "u'u" : "u",
    "o'a" : "ua",
    "u'a" : "ua",
    "u'e" : "ui",
    "u'i" : "ui",
}

coda_conversion = dict(zip('bpfvdtgkxcjszlmnr', 'bbbbddgggsssslmnr'))

def process_candidate_form(protoform, shape, gismu, gismu_shape, pos):

    form = protoform

    # Process forms
    if shape == 'CAC':
        a = form[:1]
        b = form[2]
        b2 = coda_conversion.get(b, b)
        form = f'{a}{b2}'

    elif 'AA' in shape:
        # CA(')A CCA(')A CCA(')AC
        n = 2 if shape[1] == 'C' else 1     # 2 if CC-, 1 if C-
        p = -1 if shape[-1] == 'C' else 0   # -1 if -C (ends in consonant), else 0
        a = form[:n]
        b = form[n+1:p]
        b2 = diphthong_conversion.get(b, b)
        c = form[p]

        if len(b2) == 2:
            form = f'{a}{b2}{c}'
        elif len(b2) == 1:
            form = f'{a}{b2}{gismu[3]}'
            shape = 'CAC'

    if shape.startswith('CC'):
        # CCA, CCAC: xl > kl, xr > kr
        if form[0] == 'h':
            b = form[1:]
            form = f'k{b}'

    return form


    