import src.lojban_specific.phonological_inventory as inv 
import src.lojban_specific.word_shape as shape

def determine_wordclass(s):

    wordclass = 'undetermined'

    if s[-1] in inv.C:
        wordclass = 'cmene'
    elif s[-1] in inv.A:
        if shape(s[5]) in ('CCAAC', "CCA'A", 'CACCA', 'CAACC'):
            if len(s) == 5:
                wordclass = 'gismu'
            elif len(s) > 5:
                wordclass = 'lujvo'
        else:
            if len(s) < 3 or (len(s) == 4 and "'" in s):
                wordclass = 'cmavo'
            else:
                wordclass = 'cmavo_sequence'                          

    return wordclass

def lujvo_parser(s):

    # In English: compound nouns
    # Assuming we know that the word is a lujvo

    out = list()
    while s != '':

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

        # CAA(l/n/r)-C
        elif s[3] in ('l', 'n', 'r') and s[4] in inv.C:
            out.append(s[:3])   # exclude rafsi-final hyphen
            s = s[4:]           

        # CAA, CAC, CCA - C
        elif s[3] in inv.C:
            out.append(s[:3])
            s = s[3:]

        else:
            out.append(s)
            out.append('CHECK IF LUJVO!')
            s = ''

    return out

def lujvo_parse_as_string(s):

    try:
        return '-'.join(lujvo_parser(s))
    except:
        return f'{s} !!'

def fuivla_parser(s):
    # In English: loanwords
    ...