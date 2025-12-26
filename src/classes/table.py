import pandas as pd

class Table():
	def __init__(self, filename, dir1='data/lojban1999', dir2='data', keep_default_na=True, sep=',', ext=None):

		if not ext:
			if sep == '\t':
				ext = 'tsv'
			else:
				ext = 'csv'

		self.dff = pd.read_csv(f'{dir1}/{filename}.{ext}', keep_default_na=keep_default_na, sep=sep)