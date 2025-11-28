import pandas as pd

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