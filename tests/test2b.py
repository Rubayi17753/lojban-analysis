# Lujvo parse test
from src.lojban_specific.parser import compound_cmavo_parser

def main():    

    lujvos = ("baku'anoroi", "a'ije")
    for lujvo in lujvos:
        print(f"{lujvo} {'-'.join(compound_cmavo_parser(lujvo))}")