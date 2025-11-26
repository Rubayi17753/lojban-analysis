import pandas as pd

class Table():
	def __init__(self, filename):
		self.dff = pd.read_csv(f'data/lojban1999/{filename}.csv')