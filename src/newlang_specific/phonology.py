# differences from lojban: + zn jn = xl xr

valid_cons_pairs = (
    ('pbfvkgxm', 'lr'),
    # ('csjz', 'pftkbdvgmnlr'),
    # ('td', 'csjzr'),
    ('cs', 'pftkmnlr'),
    ('z', 'bdvgmn'),
    ('j', 'bdvgmn'),
    ('t', 'csr'),
    ('d', 'jzr'),    
)

valid_cons_pairs = tuple(f'{c1}{c2}' for (cc1, cc2) in valid_cons_pairs for c1 in cc1 for c2 in cc2)

import src.newlang_specific.sound_changes as sound_changes
reduced_diphthongs = tuple(k for k, v in sound_changes.diphthongs.items() if len(v) == 1)

caac_coda_restriction = ''