import pandas as pd

class Table():
	def __init__(self, filename):
		self.df = pd.read_csv(f'data/lojban1999/{filename}.csv')
	
def main():
	curr_df = Table('freqs_gismu').df
	print(curr_df)