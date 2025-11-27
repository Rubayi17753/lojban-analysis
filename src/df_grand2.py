# Deals with freqs_lujvo1999

# import pandas as pd
# from tqdm import tqdm
import numpy as np
from src.tools.class_table import Table

def get_df_rafsi_freqs():
	df = Table('freqs_lujvo1999').dff

	def obtain_shapes(df):
		from src.rawfreq_shape import rawfreq_shape
		df['rawfreq_shapes'] = df['freq_raw'].apply(rawfreq_shape)
		df['shape_count'] = df.groupby('rawfreq_shapes')['freq_raw'].transform('count')
		# df = df.sort_values('shape_count', ascending=False)
		# df = df[['freq_raw', 'rawfreq_shapes', 'shape_count']]
		return df
	
	def obtain_lujvofreqs(df):
		from src.rawfreq_to_freq import rawfreq_to_freq
		from src.lojban_specific.parser import lujvo_parser

		# loop-based workflow for ease of tracking
		# df['actual_parsed'] = tuple(lujvo_parser(actual) for actual in tqdm(tuple(df['actual'])))
		
		df['actual_parsed'] = df['actual'].apply(lujvo_parser)
		df['freq'] = df['freq_raw'].apply(rawfreq_to_freq)
		# df = df.sort_values('shape_count', ascending=False)

		# Explode actual_parsed > rafsi
		df = df.explode('actual_parsed')

		# Post-explode ops
		df = df.rename(columns={'actual_parsed': 'rafsi', 
						'actual': 'lujvo'})

		excluded_signs = ('%', '!%')
		excluded_rafsi = ('sel', 'ter', 'vel', 'xel')
		df = df[(df['section_id'] == 11)
				& (~df['sign'].isin(excluded_signs))
				& (~df['rafsi'].isin(excluded_rafsi))
				]

		df['rafsi_pos_ind'] = df.groupby('lujvo')['lujvo'].cumcount() + 1
		df['lujvo_length'] = df.groupby('lujvo')['lujvo'].transform('count')

		# ini, med, fin
		conditions = [
			df['lujvo_length'] == 1,
			df['rafsi_pos_ind'] == 1,
			df['rafsi_pos_ind'] == df['lujvo_length'],
				]
		choices = ['conversion', 'ini', 'fin']
		df['rafsi_pos'] = np.select(conditions, choices, default='med')

		return df

	def obtain_rafsifreqs(df):

		# data regrouped by rafsi
		df = df.groupby(['rafsi', 'rafsi_pos'], as_index=False)['freq'].sum()
		
		# pivot on rafsi_pos
		df = df.pivot(index='rafsi', columns='rafsi_pos', values='freq').reset_index()

		return df

	def clean1(df):
		df = df[['lujvo', 'rafsi', 'freq', 
					'rafsi_pos', 
					'rafsi_pos_ind', 'lujvo_length', 
					'canon_meaning']]
		return df

	df = obtain_lujvofreqs(df)
	df = obtain_rafsifreqs(df)
	# df = clean1(df)	# only applicable for obtain_lujvofreqs

	return df

def main():
	df_rafsi_freqs().to_csv('results/q2.tsv', sep="\t", index=False)