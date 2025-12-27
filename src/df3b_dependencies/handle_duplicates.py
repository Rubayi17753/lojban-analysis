import pandas as pd
from src.lojban_specific.word_shape import word_shape

def handle_duplicate_forms(df, display_stats=1, sift=1):

    df['current_stem_count'] = df.groupby('current_stem')['gismu'].transform('count')
    mask_dupl = df['current_stem_count'] > 1

    if display_stats:
        dupl_count = mask_dupl.sum()
        print(f'Duplicates remaining: {dupl_count}\n')

        df['current_stem_shape'] = df['current_stem'].apply(word_shape)
        print('Form shape rundown: ')
        print(df['current_stem_shape'].value_counts())

    df['max_gismu_sum'] = df.groupby('current_stem')['gismu_sum'].transform('max')
    df['coef_gismu_sum'] = df['gismu_sum'] / df['max_gismu_sum']

    gismus = list(df['gismu'])
    current_stems = list(df['current_stem'])
    form_stacks = list(df['stack'])
    coefs = list(df['coef_gismu_sum'])
    tendencies = list(df['pos_tendency'])
    # set_current_stems = set(current_stems)

    def conditions(stack, dupl, coef, tendency):
        if sift == 1:
            return stack and dupl and coef < 0.8
        elif sift == 10:
            return stack and dupl and coef < 0.99
        elif sift == 2:
            return stack and dupl
        elif sift == 3:
            return (stack and dupl and  
                    (
                        (tendency == 'ini' and word_shape(stack[-1])[:2] == 'CC')
                        or (tendency == 'fin' and word_shape(stack[-1])[-2:] == 'CC')
                    ))

    cur_forms, stacks = list(), list()
    n_changes = 0
    for g, cur_form, stack, dupl, coef, tendency in zip( gismus, current_stems, form_stacks, mask_dupl, coefs, tendencies ):
        if conditions(stack, dupl, coef, tendency):
            a = stack[-1]
            if a and a not in current_stems:
                cur_form = stack.pop()
                n_changes += 1
            else:
                stack.pop()
        cur_forms.append(cur_form)
        stacks.append(stack)

    if display_stats:
        print(f'{n_changes} forms changed')

    df['current_stem'] = pd.Series(cur_forms)
    df['stack'] = pd.Series(stacks)
    df['current_stem_count'] = df.groupby('current_stem')['gismu'].transform('count')

    return df

def handle_duplicate_df(df):
    df['current_stem'] = df['stack'].str[-1]
    df['stack'] = df['stack'].str.slice(stop=-1)

    df = handle_duplicate_forms(df)
    df = handle_duplicate_forms(df, sift=3)
    df = handle_duplicate_forms(df)
    
    for i in range(8):
        df = handle_duplicate_forms(df, sift=10)
    for i in range(8):
        df = handle_duplicate_forms(df, sift=2)
    
    return df