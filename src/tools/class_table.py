import pandas as pd

class Table():
	def __init__(self, filename, keep_default_na=True):
		self.dff = pd.read_csv(f'data/lojban1999/{filename}.csv', keep_default_na=keep_default_na)