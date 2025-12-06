# differences from lojban: + zn jn = xl xr

valid_cons_pairs = (
    ('pbfvkgm', 'lr'),
    ('cs', 'pftkmnlr'),
    ('jz', 'bdvgmn'),
    ('t', 'csr'),
    ('d', 'jzr'),
)

valid_cons_pairs = tuple(f'{c1}{c2}' for (cc1, cc2) in valid_cons_pairs for c1 in cc1 for c2 in cc2)

