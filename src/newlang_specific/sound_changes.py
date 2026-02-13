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
    "i'u" : "io",
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
    "u'i" : "ue",
}

diphthongs.update({k.replace("'", "") : v for k, v in diphthongs.items()})

cons_coda_cac = dict(zip('bpvfdtgkxcjszlmnr', 'ppppltkkkttsslmnr'))
cons_coda_cac2 = dict(zip('bpvfdtgkxcjszlmnr', 'mpppttkkksssslmnr'))
cons_coda_caac = dict(zip('bpvfdtgkxcjszlmnr', 'bbvvddgggddzzlmnr'))
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

hyphens_aa2 = coda_stem_to_lemma[hyphens_aa]

def stem_to_combining(x, sh=None):
    if x:

        if not sh:
            sh = word_shape.word_shape(x)
        
        infix = ''
        if sh == 'CAAC':
            if x[-1] != 'n':
                infix = hyphens_aac
        elif sh == 'CAA':
            infix = 'n'

        x = f'{x}{infix}'

    return x

def stem_to_lemma(x, sh=None):

    if x:
        if not sh:
            sh = word_shape.word_shape(x)
        coda = x[-1]
        
        xc = stem_to_combining(x, sh)

        infix = ''
        if sh == 'CA':
            infix = 'dv'
        elif sh == 'CCA':
            infix = hyphens_ca
        elif sh == 'CAA':
            x, infix = xc[:-1], hyphens_aa2
        elif sh == 'CCAA':
            infix = hyphens_aa
        elif sh == 'CAC':
            x, infix = xc[:-1], coda_stem_to_lemma.get(coda, coda)
        elif sh == 'CAAC':
            x, infix = x.strip(hyphens_aac), ''
            print(x)

        x = f'{x}{infix}'  
        x = stem_to_combining(x).strip(hyphens_cc).strip(hyphens_aac)
        x = f'{x}a'

    return x