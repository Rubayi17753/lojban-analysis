import re

# x[x]
pattern = re.compile(r'^\d+\[\d+\]$')

def rawfreq_to_freq(s):

	freq = 0

	if s.startswith('<'):
		pass

	else:

		for sub in s.split('+'):
			try:
				if sub.isnumeric():
					freq += int(sub)

				elif pattern.fullmatch(s):
					x, y = sub.strip(']').split('[')

					if x != y:
						print(sub)
			except:
				print(sub)

	return freq