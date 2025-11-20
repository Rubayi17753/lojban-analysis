# Lujvo parse test
from src.lojban_specific.parser import lujvo_parser

def main():    

    lujvos = ("nalcumselfanva",
                "laurba'u",
                "ctejau",
                "tinju'i",
                "snavelminra",
                "jdapli",
                "mosycpu",
                "terdargu",
                "sacrai",
                "velkancu",)
    for lujvo in lujvos:
        print(f"{lujvo} {'-'.join(lujvo_parser(lujvo))}")