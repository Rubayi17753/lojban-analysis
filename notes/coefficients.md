coef1 :
- df['coef1'] = round(df['form_freq'] / df['max_form_freq'] * 100 , 1)
- Shows how 'often' a certain form is used
coef2 :
- df['coef2'] = round( np.log10(df['percentage_fm'] / df['percentage_im']) , 2)
- df['coef2'] = df['coef2'] * (1 - 1 / math.sqrt((df['as_rafsi']) + 0.01)) 
- (positional tendency) with attestation accounted for
coef3 :
- df['max_coef'] = df.groupby('gismu')['form_overridden'].transform('max')
- df['coef3'] = df['coef1_1'] / df['max_coef']
- coef1's derivation algorithm reapplied to coef1
coef_gismu_sum :
- df['max_gismu_sum'] = df.groupby('current_stem')['gismu_sum'].transform('max')
- df['coef_gismu_sum'] = df['gismu_sum'] / df['max_gismu_sum']
- df3b.handle_duplicate_forms