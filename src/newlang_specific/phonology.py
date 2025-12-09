# differences from lojban: + zn jn = xl xr

valid_cons_pairs = (
    ('pbfvkgm', 'lr'),
    ('csjz', 'pftkbdvgmnlr'),
    ('td', 'csjzr'),
)

valid_cons_pairs = tuple(f'{c1}{c2}' for (cc1, cc2) in valid_cons_pairs for c1 in cc1 for c2 in cc2)

import src.newlang_specific.conversion as conv
reduced_diphthongs = tuple(k for k, v in conv.diphthongs.items() if len(v) == 1)