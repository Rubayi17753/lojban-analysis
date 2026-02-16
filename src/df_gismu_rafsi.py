# Deals with defs_rafsi

import pandas as pd
from src.classes.table import Table

def get_df_gismu_rafsi():
	df = Table('defs_rafsi', keep_default_na=False).dff		# Prevents pandas for reading string 'nan' as NaN
	dfg = Table('defs_gismu').dff

	df5 = (dfg[['gismu', 'gismu']])
	df5.columns = ['rafsi', 'gismu']
	
	df4 = df5.copy()
	df4['rafsi'] = df4['rafsi'].str.slice(start=0, stop=4)

	df = pd.concat([df, df4, df5], axis=0)
	df = df[['rafsi', 'gismu']]

	

	return df

def main():
	get_df_gismu_rafsi()