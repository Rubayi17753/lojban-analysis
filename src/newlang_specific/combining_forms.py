import src.lojban_specific.phonological_inventory as inv
import src.lojban_specific.word_shape as word_shape

hyphens = {'digram' : 'dv',
    'cmavo' : 'ḟ',
    'cacc' : '’',
    'aac' : '′',
    'cca' : 'l',
    'lemma' : 'a',
    'aa1' : 'n',
    'aa2' : 'ng',
    'ccaa' : 'v',
}

coda_stem_to_lemma = {
    'p': 'pr', 't': 'tc', 'k': 'kr',
    'f': 'ft', 's': 'st',
    'l': 'lg', 'm': 'mb', 'n': 'nd', 'r': 'rv',

    'b': 'bl', 'g': 'gl', 'v': 'vl', 'z': 'dz',
}

def stem_to_combining(x, sh=None):
    if x:

        if not sh:
            sh = word_shape.word_shape(x)
        
        infix = ''
        if sh == 'CAAC':
            if x[-1] != 'n':
                infix = hyphens['aac']
        elif sh == 'CACC':
            infix = hyphens['cacc']
        elif sh == 'CAA':
            infix = hyphens['aa1']

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
            infix = hyphens['cca']
        elif sh == 'CAA':
            x, infix = xc[:-1], hyphens['aa2']
        elif sh == 'CCAA':
            infix = hyphens['ccaa']
        elif sh == 'CAC':
            x, infix = xc[:-1], coda_stem_to_lemma.get(coda, coda)
        elif sh == 'CAAC':
            x, infix = x.strip(hyphens['aac']), ''
            # print(x)

        x = f'{x}{infix}'  
        x = stem_to_combining(x).strip(hyphens['cacc']).strip(hyphens['aac'])
        # x = f'{x}a'

    return x