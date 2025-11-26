# Deals with freqs_lujvo1999

import pandas as pd
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
		df['freq'] = df['freq_raw'].apply(rawfreq_to_freq)
		# df = df.sort_values('shape_count', ascending=False)
		# df = df[['freq_raw', 'rawfreq_shapes', 'shape_count']]
		return df

	df = obtain_rawfreqs(df)
	return df

def main():
	process_lujvo1999().to_csv('results/q2.tsv', sep="\t", index=False)