import config.threshholds as th

def determine_pos_tendency(df):
    # Determine rafsi positioning tendency
    # Requires dfq1() --> coef2

    # Sanitisation

    for col in ('as_rafsi', 'percentage_im', 'percentage_fm', 'coef2'):
        df[col] = (pd.to_numeric(df[col], errors='coerce')
        .replace(np.inf, 999)
        .replace(-np.inf, -999)
        )

    df = df.fillna(0)

    conditions = [
        (df['as_rafsi'] == 0).astype(bool),
        (df['percentage_im'] == 0).astype(bool),
        (df['percentage_fm'] == 0).astype(bool),
        (df['coef2'] > th.coef2_threshhold).astype(bool),
        (df['coef2'] < -th.coef2_threshhold).astype(bool),
            ]
    choices = ['??', 'fin', 'ini', 'fin', 'ini']
    df['pos_tendency'] = np.select(conditions, choices, default='neut')

    return df