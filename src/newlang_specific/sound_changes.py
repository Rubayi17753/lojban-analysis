import src.lojban_specific.phonological_inventory as inv

diphthongs = {
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
    "i'o" : "io",
    "i'u" : "io",
    "o'o" : "o",
    "o'u" : "o",
    "o'e" : "oi",
    "o'i" : "oi",
    "oi" : "oi",
    "u'o" : "u",
    "u'u" : "u",
    "o'a" : "ua",
    "u'a" : "ua",
    "u'e" : "ue",
    "u'i" : "ue",
}

diphthongs.update({k.replace("'", "") : v for k, v in diphthongs.items()})

cons_coda = dict(zip('bpfvdtgkxcjszlmnr', 'ppffttkkksssslfnr'))

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
clusters_fin.update(cons_coda)