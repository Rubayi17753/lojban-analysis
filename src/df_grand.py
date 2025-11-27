import pandas as pd
from src.tools.class_table import Table

def process_freqs_cmavo2():
	from src.lojban_specific.parser import compound_cmavo_parser
	df = Table('freqs_cmavo2').dff

	# excludes dubious items
	df = df[ df['dubious'].isna() ]	
	df = df[ ~df['cmavo_composite'].str.startswith('*') ]

	df['cmavo_composite2'] = df['cmavo_composite'].transform(compound_cmavo_parser)
	df = df.explode('cmavo_composite2')
	df = df.rename( columns={'cmavo_composite2' : 'cmavo'} )

	df2 = df.groupby('cmavo').agg(
		freq=('freq', 'sum'),
		composites=('cmavo_composite', ' '.join)
		).reset_index()

	print('freqs_cmavo2 processed')
	return df2

def create_grand_table():

	from src.df_grand2 import get_df_rafsi_freqs

	df1 = (Table('defs_cmavo')
			.dff[['cmavo', 'gismu', 'class']])
	df1 = df1[df1['gismu'].notna() & (df1['gismu'] != '.')]

	df2 = Table('defs_rafsi').dff[['rafsi', 'gismu']]

	# Rename & merge
	df1.columns = ['cmavo_rafsi', 'gismu', 'class']
	df2.columns = ['cmavo_rafsi', 'gismu']
	df_rafsi_freqs = get_df_rafsi_freqs()
	df_rafsi_freqs = df_rafsi_freqs[['rafsi', 'ini', 'med', 'fin', 'conversion']]
	df_rafsi_freqs.columns = ['rafsi', 'as_rafsi_i', 'as_rafsi_m', 'as_rafsi_f', 'as_rafsi_conv']

	df3 = (pd.concat([df1[['cmavo_rafsi', 'gismu']], df2], ignore_index=True)
			.drop_duplicates()

			.merge(df1[['cmavo_rafsi', 'gismu', 'class']], 
			left_on=['cmavo_rafsi', 'gismu'], 
			right_on=['cmavo_rafsi', 'gismu'], 
			how='outer')

			.merge(df_rafsi_freqs, 
			left_on='cmavo_rafsi', 
			right_on='rafsi', 
			how='outer')			
			)

	def merge_freqs(df3):
		df_cmavo1 = Table('freqs_cmavo1').dff[['cmavo', 'freq']]
		df_cmavo2 = process_freqs_cmavo2()
		df_gismu = Table('freqs_gismu').dff[['gismu', 'freq']]

		df_cmavo1 = df_cmavo1.rename(columns={'freq': 'as_cmavo'})
		df_cmavo2 = df_cmavo2.rename(columns={'freq': 'as_cmavo_compound'})
		df_gismu = df_gismu.rename(columns={'freq': 'as_gismu'})

		# Merge with template
		df3 = (df3[df3['class'].notna()]
				.merge(df_cmavo1[['cmavo', 'as_cmavo']], 
					left_on='cmavo_rafsi', 
					right_on='cmavo', 
					how='left')
				.merge(df_cmavo2[['cmavo', 'as_cmavo_compound']], 
					left_on='cmavo_rafsi', 
					right_on='cmavo', 
					how='left')
				)
		df3 = pd.concat([df3, df_gismu], axis=0)

		return df3
	
	def clean(df3):
		freq_cols = ['as_gismu', 
					'as_rafsi_conv', 'as_rafsi_i', 'as_rafsi_m', 'as_rafsi_f', 
					'as_cmavo', 'as_cmavo_compound',]

		df3 = (df3
				.drop_duplicates()
				.fillna({
					col: 0
					for col in df3[freq_cols]})
				.sort_values(['gismu', 'cmavo_rafsi'], ascending=[True, True])
				)
		df3[freq_cols] = df3[freq_cols].astype('Int64')
		df3 = df3[['gismu', 'cmavo_rafsi', 'class',
					'as_gismu', 
					'as_rafsi_conv', 'as_rafsi_i', 'as_rafsi_m', 'as_rafsi_f', 
					'as_cmavo', 'as_cmavo_compound',]]
		
		return df3
	
	df3 = merge_freqs(df3)
	df3 = clean(df3)

	return df3

def main():
	create_grand_table().to_csv('results/q1.tsv', sep="\t", index=False)