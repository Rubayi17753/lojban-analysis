import src.lojban_specific.phonological_inventory as inv 

def determine_wordclass(s):
    if s[-1] in C:
        return 'cmene'
    elif s[-1] in A:
        if len == 5:
            return 'lujvo'                                
    else:
        return '???'

def lujvo_parser(s):

    # In English: compound nouns
    # Assuming we know that the word is a lujvo

    out = list()
    while s != '':

        # finals
        if len(s) in (3, 4, 5):
            out.append(s)
            s = '' 

        # CA'A-C
        elif s[2] == "'" and s[4] in inv.C:
            out.append(s[:4])
            s = s[4:]

        # CACy-C 
        elif s[3] == 'y' and s[4] in inv.C:
            out.append(s[:3])   # exclude rafsi-final -y
            s = s[4:]

        # CACCy-C, CCACy-C
        elif s[4] == 'y' and s[5] in inv.C:
            out.append(s[:4])   # exclude rafsi-final -y
            s = s[5:]

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
    return '-'.join(lujvo_parser(s))

def fuivla_parser(s):
    # In English: loanwords
    ...