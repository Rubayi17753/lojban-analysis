# Deals with freqs_lujvo1999

import pandas as pd
from tqdm import tqdm
from src.tools.class_table import Table

def df_gismu_rafsi():
	df = Table('defs_rafsi').dff

	df5 = (df[['gismu', 'gismu']])
	df5.columns = ['rafsi', 'gismu']
	
	df4 = df5.copy()
	df4['rafsi'] = df4['rafsi'].str.slice(start=0, stop=4)

	df = pd.concat([df, df4, df5], axis=0)
	df = df[['rafsi', 'gismu']]

	return df

def main():
	print(df_rafsi_complete().sample(20))

if __name__ == '__main__':
	main()