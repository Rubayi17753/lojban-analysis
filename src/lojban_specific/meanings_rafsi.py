import pandas as pd

def get_df_rafsi_meaning():
	
	from src.classes.table import Table
	from src.lojban_specific.meanings_gismu import get_df_gismu_meaning

	df = Table('defs_rafsi', keep_default_na=False).dff		# Prevents pandas for reading string 'nan' as NaN
	dfg = Table('defs_gismu').dff

	dfg = get_df_gismu_meaning(dfg)

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

meanings_rafsi = get_df_rafsi_meaning().set_index('rafsi')['meaning'].to_dict()