
from src.lojban_specific.parser import lujvo_parser

def lujvo_parse_as_string(s):

    try:
        return '-'.join(lujvo_parser(s))
    except:
        return f'{s} !!'

def lujvo_length(s):

    try:
        return len(lujvo_parser(s))
    except:
        return -999