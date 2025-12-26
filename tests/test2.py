# Lujvo parse test
from src.lojban_specific.parser import lujvo_parser

def main():    

    lujvos = ("dutyku'arka",)
    for lujvo in lujvos:
        print(f"{lujvo} {'-'.join(lujvo_parser(lujvo))}")