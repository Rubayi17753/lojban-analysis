import pandas as pd

class Table():
	def __init__(self, filename):
		self.dff = pd.read_csv(f'data/lojban1999/{filename}.csv')

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

	df3 = df.groupby('cmavo')['cmavo_composite'].agg(' '.join)

	print(df2)

def create_grand_table():
	df1 = (Table('defs_cmavo')
			.dff[['cmavo', 'gismu', 'class']])
	df1 = df1[df1['gismu'].notna() & (df1['gismu'] != '.')]

	df2 = Table('defs_rafsi').dff[['rafsi', 'gismu']]

	# Rename & merge
	df1.columns = ['cmavo_rafsi', 'gismu', 'class']
	df2.columns = ['cmavo_rafsi', 'gismu']

	df3 = (pd.concat([df1[['cmavo_rafsi', 'gismu']], df2], ignore_index=True)
			.drop_duplicates()
			.merge(df1[['cmavo_rafsi', 'gismu', 'class']], 
			left_on=['cmavo_rafsi', 'gismu'], 
			right_on=['cmavo_rafsi', 'gismu'], 
			how='outer'))

	return df3

def main():
	create_grand_table().to_csv('results/q1.tsv', sep="\t", index=False)