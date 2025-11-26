# Deals with freqs_lujvo1999

# import pandas as pd
# from tqdm import tqdm
from src.tools.class_table import Table

def process_lujvo1999():
	df = Table('freqs_lujvo1999').dff

	def obtain_shapes(df):
		from src.rawfreq_shape import rawfreq_shape
		df['rawfreq_shapes'] = df['freq_raw'].apply(rawfreq_shape)
		df['shape_count'] = df.groupby('rawfreq_shapes')['freq_raw'].transform('count')
		# df = df.sort_values('shape_count', ascending=False)
		# df = df[['freq_raw', 'rawfreq_shapes', 'shape_count']]
		return df
	
	def obtain_rawfreqs(df):
		from src.rawfreq_to_freq import rawfreq_to_freq
		from src.lojban_specific.parser import lujvo_parser

		# loop-based workflow for ease of tracking
		# df['actual_parsed'] = tuple(lujvo_parser(actual) for actual in tqdm(tuple(df['actual'])))
		
		df['actual_parsed'] = df['actual'].apply(lujvo_parser)
		df['freq'] = df['freq_raw'].apply(rawfreq_to_freq)
		# df = df.sort_values('shape_count', ascending=False)

		# Explode actual_parsed > rafsi
		df = df.explode('actual_parsed')
		
		return df


	def clean(df):
		df = df[df['section_id'] == 11]
		df = df[['actual', 'actual_parsed', 'freq_raw', 'freq', 'canon_meaning']]
		return df

	df = obtain_rawfreqs(df)
	df = clean(df)
	return df

def main():
	process_lujvo1999().to_csv('results/q2.tsv', sep="\t", index=False)