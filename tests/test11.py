# Test utils.duplicates_to_blank
from src import utils

def main():
    print(utils.duplicates_to_blank(['a', '', '', 'a', 'b', 'a', 'b', '', 'b', '']))