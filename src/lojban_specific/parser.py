import pandas as pd
import src.lojban_specific.phonological_inventory as inv 
import src.lojban_specific.word_shape as shape

def get_df_rafsi_meaning():
	
	from src.tools.class_table import Table

	df = Table('defs_rafsi', keep_default_na=False).dff		# Prevents pandas for reading string 'nan' as NaN
	dfg = Table('defs_gismu').dff

	# Handles meanings of the format wood ‘lumber’
	dfg['meaning'] = dfg['meaning'].str[1:-1]
	dfg[['meaning', 'mnemonic']] = dfg['meaning'].str.split(' ‘', n=1, expand=True)
	dfg['mnemonic'] = dfg['meaning'].str[:-1]

	df5 = (dfg[['gismu', 'gismu']])
	df5.columns = ['rafsi', 'gismu']
	
	df4 = df5.copy()
	df4['rafsi'] = df4['rafsi'].str.slice(start=0, stop=4)

	df = pd.concat([df, df4, df5], axis=0)

	df = df.merge(dfg[['gismu', 'meaning']], 
			left_on='gismu', 
			right_on='gismu', 
			how='left')

	df['meaning'] = df['meaning_y'].fillna(df['meaning_x'])
	df = df[['rafsi', 'meaning']]

	return df

rafsi_meanings = get_df_rafsi_meaning().set_index('rafsi')['meaning'].to_dict()

def determine_wordclass(s):

    wordclass = 'undetermined'

    if s[-1] in inv.C:
        wordclass = 'cmene'
    elif s[-1] in inv.A:

        if 'CC' in shape(s[5]):

            if 'CC' in shape(s[-5:]):
                if len(s) == 5:
                    wordclass = 'gismu'
                elif len(s) > 5:
                    wordclass = 'lujvo'
            else:
                wordclass = 'fu_ivla'

        else:
            if len(s) < 3 or (len(s) == 4 and "'" in s):
                wordclass = 'cmavo'
            else:
                wordclass = 'cmavo_sequence'                          

    return wordclass

def lujvo_parser(s):

    # In English: compound nouns

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
                    print(s)
                    out.append(s)
                    out.append('CHECK IF LUJVO!')
                    s = ''                   

            # CAA(l/n/r)-C
            elif s[3] in ('l', 'n', 'r') and s[4] in inv.C:
                out.append(s[:3])   # exclude rafsi-final hyphen
                s = s[4:]           

            # CAA, CAC, CCA - C
            elif s[3] in inv.C:
                out.append(s[:3])
                s = s[3:]

            else:
                print(s)
                out.append(s)
                out.append('CHECK IF LUJVO!')
                s = ''
        
        except:
            print(f'Check if lujvo: {s}')

    return out

def lujvo_breakdown(s, parsed=True):

    if not parsed:
        s = lujvo_parser(s)
    print((rafsi_meanings.get(rafsi, s) for rafsi in s))
    return (rafsi_meanings.get(rafsi, s) for rafsi in s)

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