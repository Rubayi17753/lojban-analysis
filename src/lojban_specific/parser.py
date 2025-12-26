import re
import pandas as pd
import src.lojban_specific.phonological_inventory as inv 
from src.lojban_specific.word_shape import word_shape
from src.lojban_specific.meanings_rafsi import meanings_rafsi

def determine_wordclass(s):

    wordclass = 'undetermined'

    if s[-1] in inv.C:
        wordclass = 'cmene'
    elif s[-1] in inv.A:

        z = s.replace("'", '')
        x5_ini = word_shape(z[:5])
        if 'CC' in x5_ini or 'y' in (s[3], s[4]):

            if len(s) == 5 and s[0] in inv.C:
                wordclass = 'gismu'
            else:
                x3_fin1 = word_shape(z[-3:])
                x3_fin2 = word_shape(z[-6:-3])
                x5_fin = word_shape(z[-5:])
                test1a = x3_fin1 in ('AAC', 'CAC', 'CCA')
                test1b = x3_fin2 in ('CAA', 'CAC', 'CCA')
                test2 = 'CC' in word_shape(x5_fin)
                if (test1a and test1b) or test2 and s[0] in inv.C:
                    wordclass = 'lujvo'
                else:
                    wordclass = 'fu_ivla'

        else:
            if len(z) <= 3:
                wordclass = 'cmavo'
            else:
                wordclass = 'cmavo_sequence'                          

    return wordclass

def lujvo_parser(s, noisy=1):

    # In English: compound nouns

    lujvo = f'{s}'
    out = list()
    while s != '':

        try:

            # finals
            if len(s) in (3, 4, 5):
                out.append(s)
                s = '' 

            # CACy-C 
            elif s[3] == 'y' and s[4] in inv.C:
                out.append(s[:3])   # exclude rafsi-final -y
                s = s[4:]

            # CACCy-C, CCACy-C
            elif s[4] == 'y' and s[5] in inv.C:
                out.append(s[:4])   # exclude rafsi-final -y
                s = s[5:]

            elif s[2] == "'":

                # CA'A(l/n/r)-C
                if s[4] in ('l', 'n', 'r') and s[5] in inv.C:
                    out.append(s[:4])   # exclude rafsi-final hyphen
                    s = s[5:]
                
                # CA'A-C
                elif s[2] == "'" and s[4] in inv.C:
                    out.append(s[:4])
                    s = s[4:]

                else:
                    print(f'Check if lujvo: {lujvo}; {s} unparseable')
                    # out.append(s)
                    # out.append('CHECK IF LUJVO!')
                    s = ''                   

            # CAA(l/n/r)-C
            elif s[3] in ('l', 'n', 'r') and s[4] in inv.C:
                out.append(s[:3])   # exclude rafsi-final hyphen
                s = s[4:]           

            # CAA, CAC, CCA - C
            elif s[3] in inv.C:
                out.append(s[:3])
                s = s[3:]

            elif len(s) <= 2:
                s = ''
                if noisy:
                    print(f'Check if lujvo: {lujvo}; {s} unparseable')
                break               

            else:
                if noisy:
                    print(f'Check if lujvo: {lujvo}; {s} unparseable')
                out.append(s)
                # out.append('CHECK IF LUJVO!')
                s = ''
        
        except:
            if noisy:
                print(f'Check if lujvo: {lujvo}')
            break

    return out

def lujvo_breakdown(s, parsed=True):

    try:
        if not parsed:
            s = lujvo_parser(s)
        return tuple(meanings_rafsi.get(rafsi, s) for rafsi in s)
    except:
        return ''

def compound_cmavo_parser(s, delim=None):

    # if delim=None, return list
    out = list()
    len_str = len(s)

    for char1, char2 in zip(s[0 : len_str-1], s[1 : len_str]):
        if char1 in inv.A and char2 in inv.C:
            s = s.replace(f'{char1}{char2}', f'{char1}_{char2}')

    if delim == None:   
        return s.split('_')
    else:
        return s.replace('_', delim)

def fuivla_parser(s):
    # In English: loanwords
    ...

def syllable_parser(s, delim=None):
    
    out = list()
    len_str = len(s)

    for char1, char2 in zip(s[0 : len_str-1], s[1 : len_str]):
        if char1 in inv.A and char2 in inv.C:
            s = s.replace(f'{char1}{char2}', f'{char1}_{char2}')
        elif char1 in inv.C and char2 in inv.A:
            s = s.replace(f'{char1}{char2}', f'{char1}_{char2}')

    if '__' in s:
        s = re.sub(r'_+', '_', s)
    if delim == None:   
        return s.split('_')
    elif delim != '_':
        return s.replace('_', delim)