import re

# x[x]
pattern1 = re.compile(r'^\[\d+\]$')
pattern2 = re.compile(r'^\d+\[\d+\]$')

def rawfreq_to_freq(s):

	freq = 0

	if s.startswith('<'):
		pass

	else:

		for sub in s.split('+'):
			try:
				if sub.isnumeric():
					freq += int(sub)

				elif pattern1.fullmatch(sub):
					freq += int(sub[1:-1])

				elif pattern2.fullmatch(sub):
					x, y = sub.rstrip(']').split('[')

					if x != y:
						print(s)
			except:
				print(s)

	return freq