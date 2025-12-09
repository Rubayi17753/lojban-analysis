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

clusters_l = (
    ('bdgv', 'ptkf', 'bpfvdtgkxcjszmn'),
    ('zj', 'cs', 'bpfvdtgkxcjsz'),
    ('x', 'k', 'bpfvdtgkxcjszmn'),
    ('x', 'k', 'lr'),
    )
clusters_r = (
    ('bpfvdtgkxcjszmn', 'x', 'k'),
    ('lr', 'x', 'k'),
    )
clusters = {f'{x}{z}' : f'{y}{z}' for xx, yy, zz in clusters_l for z in zz for x, y in zip(xx, yy)}
clusters.update({f'{x}{y}' : f'{x}{z}' for xx, yy, zz in clusters_r for x in xx for y, z in zip(yy, zz)})