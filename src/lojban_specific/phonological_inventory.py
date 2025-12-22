C = 'bcdfgjklmnprstvwxz'
A = 'aeiouy'

char_type = {char : 'C' for char in C}
char_type.update({char : 'A' for char in A})
char_type["'"] = ''