import src.lojban_specific.phonological_inventory as inv
import src.lojban_specific.word_shape as word_shape
import config.hyphens as hyphens

hyphens_cc = hyphens.cc
hyphens_ca = hyphens.ca
hyphens_aa = hyphens.aa
hyphens_aac = hyphens.aac

diphthongs = {
    "a'a" : "a",
    "a'e" : "e",
    "a'i" : "ai",
    "ai" : "ai",
    "a'o" : "o",
    "a'u" : "au",
    "au" : "au",
    "e'e" : "e",
    "e'i" : "e",
    "ei" : "e",
    "e'o" : "eu",
    "e'u" : "eu",
    "i'e" : "i",
    "i'i" : "i",
    "e'a" : "e",
    "i'a" : "ia",
    "i'o" : "io",
    "i'u" : "eu",
    "o'o" : "o",
    "o'u" : "o",
    "o'e" : "oi",
    "o'i" : "oi",
    "oi" : "oi",
    "u'o" : "u",
    "u'u" : "u",
    "o'a" : "o",
    "u'a" : "ua",
    "u'e" : "ue",
    "u'i" : "oi",
}

diphthongs.update({k.replace("'", "") : v for k, v in diphthongs.items()})

cons_coda_cac = dict(zip('bpvfdtgkxcjszlmnr', 'mprrltnkkttsslmnr'))
cons_coda_caac = dict(zip('bpvfdtgkxcjszlmnr', 'ppppddnkkddsslmnr'))
cons_coda_ccac = dict(zip('bpvfdtgkxcjszlmnr', 'ppppttkkksssslmnr'))
# cons_coda_alt = dict(zip('bpvfdtgkxcjszlmnr', 'ppppttkkksssslmnr'))

clusters_ini = (
    (('x', inv.C) , ('k', inv.C)),
    (('cs', 'bdgv') , ('cs', 'ptkf')),
    (('jz', 'ptkf') , ('jz', 'bdgv')),
    (('d', 'cs') , ('d', 'jz')),
    (('t', 'jz') , ('t', 'cs')),
)

clusters_fin = (
    (('bdgv', 'pftkcsxmn') , ('ptkf', 'pftkcsxmn')),
    (('ptkf', 'bvdgjz') , ('bdgv', 'bvdgjz')),
    (('zj', 'bpfvdtgkxcjsz') , ('sc', 'bpfvdtgkxcjsz')),
    (('x', 'bpfvdtgkxcjszmnlr') , ('k', 'bpfvdtgkxcjszmnlr')),
    (('bpfvdtgkxcjszmnlr', 'x') , ('bpfvdtgkxcjszmnlr', 'k')),
)

clusters_ini = {f'{p}{q}' : f'{x}{y}' for (pp, qq), (xx, yy) in clusters_ini
                for p, x in zip(pp, xx) for q, y in zip(qq, yy)}
clusters_fin = {f'{p}{q}' : f'{x}{y}' for (pp, qq), (xx, yy) in clusters_fin
                for p, x in zip(pp, xx) for q, y in zip(qq, yy)}

coda_stem_to_lemma = {
    'p': 'pr', 't': 'tc', 'k': 'kr',
    'f': 'ft', 's': 'st',
    'l': 'ld', 'm': 'mb', 'n': 'ng', 'r': 'rv',
}

def stem_to_combining(x, sh=None):
    if x:
        if not sh:
            sh = word_shape.word_shape(x)
        if sh.endswith('CC'):
            x = f'{x}{hyphens_cc}'
        if sh.endswith('AAC'):
            if x[-1] != 'n':
                x = f'{x}{hyphens_aac}'
    return x

def stem_to_lemma(x, sh=None):

    if x:
        if not sh:
            sh = word_shape.word_shape(x)
        coda = x[-1]
        
        x = stem_to_combining(x, sh)

        infix = ''
        if sh == 'CA':
            infix = 'dv'
        elif sh.endswith('CA'):
            infix = hyphens_ca
        elif sh.endswith('AA'):
            infix = ''  # hyphens_aa
        if not sh.startswith('CC'):
            infix = coda_stem_to_lemma.get(infix, '')
            if sh.endswith('AC'):
                x = x[:-1]
                infix = coda_stem_to_lemma.get(coda, coda)

        x = f'{x}{infix}'    
        x = f'{stem_to_combining(x).strip(hyphens_cc)}a'

    return x