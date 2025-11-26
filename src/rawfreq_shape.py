import re

def rawfreq_shape(s):
	s = re.sub(r'\d', 'x', s)
	s = re.sub(r'x+', 'x', s)
	return s
