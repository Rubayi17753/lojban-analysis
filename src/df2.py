# Deals with freqs_lujvo1999

# import pandas as pd
# from tqdm import tqdm
import numpy as np
from src.tools.class_table import Table

def filter1(df):
	df = df[(df['section_id'] == 11)]	
	return df

def filter2(df):

	excluded_signs = ('%', '!%')
	excluded_rafsi = ('sel', 'ter', 'vel', 'xel',
						'dum', 'jez', 'kam', 'liz', 'muf', 'nil', 'nun', 'puv', 'siz', 'suv', 'zaz', 'zum',
						)
	df = df[
		(~df['sign'].isin(excluded_signs))
		& (~df['rafsi'].isin(excluded_rafsi))
		]
	return df

def obtain_shapes(df):
	from src.rawfreq_shape import rawfreq_shape
	df['rawfreq_shapes'] = df['freq_raw'].apply(rawfreq_shape)
	df['shape_count'] = df.groupby('rawfreq_shapes')['freq_raw'].transform('count')
	# df = df.sort_values('shape_count', ascending=False)
	# df = df[['freq_raw', 'rawfreq_shapes', 'shape_count']]
	return df

def obtain_lujvofreqs(df):
	from src.rawfreq_to_freq import rawfreq_to_freq
	from src.lojban_specific.parser import lujvo_parser, lujvo_breakdown

	# loop-based workflow for ease of tracking
	# df['actual_parsed'] = tuple(lujvo_parser(actual) for actual in tqdm(tuple(df['actual'])))
	# lambda x: myfunc(x, param1, param2)

	df['actual_parsed'] = df['actual'].apply(lujvo_parser)
	df['freq'] = df['freq_raw'].apply(rawfreq_to_freq)
	# df = df.sort_values('shape_count', ascending=False)

	# More columns for concordance
	df['breakdown'] = df['actual_parsed'].apply(lujvo_breakdown).str.join('-')
	df = df.rename(columns={'canon_meaning': 'meaning',})
	df['meaning'] = df['meaning'].fillna('').str.strip()
	
	# Explode and rename actual_parsed > rafsi
	df = df.explode('actual_parsed')
	df = df.rename(columns={'actual_parsed': 'rafsi', 
				'actual': 'lujvo'})
	
	return df

def post_explode(df):

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

def obtain_concordance(df):

	df['lujvo_and_breakdown'] = df['lujvo'] + ' : ' + df['breakdown'] + ' : ' + df['meaning']
	df = df.sort_values('freq', ascending=False)

	# data regrouped by rafsi
	df = df.groupby(['rafsi', 'rafsi_pos'], as_index=False).agg({
		'lujvo_and_breakdown': list,
	})

	df['lujvo_and_breakdown'] = df['lujvo_and_breakdown'].str.join('/')

	# pivot on rafsi_pos
	df = df.pivot(index='rafsi', columns='rafsi_pos', values='lujvo_and_breakdown').reset_index()

	df = merge_with_gismu(df)
	df = df.sort_values('gismu', ascending=True)
	df = df[['rafsi', 'gismu', 'conversion', 'ini', 'med', 'fin',]]
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

def merge_with_gismu(df):
	from src.df_gismu_rafsi import get_df_gismu_rafsi
	df_gismu_rafsi = get_df_gismu_rafsi()
	df = df.merge(df_gismu_rafsi, 
			left_on='rafsi', 
			right_on='rafsi', 
			how='left')
	return df

def get_df_rafsi_freqs():
	df = Table('freqs_lujvo1999').dff

	df1 = filter1(df)
	df1 = obtain_lujvofreqs(df1)
	df1 = filter2(df1)
	df1 = post_explode(df1)
	
	df2 = obtain_rafsifreqs(df1)
	df_fin = merge_with_gismu(df2)
	# df = clean1(df)	# only applicable for obtain_lujvofreqs

	return df_fin, df1

def main():

	df_fin, df1 = get_df_rafsi_freqs()
	df_concordance = obtain_concordance(df1)

	df_fin.to_csv('results/df2a.csv', sep=',', index=False)
	df_concordance.to_csv('results/df2b.csv', sep=',', index=False)
