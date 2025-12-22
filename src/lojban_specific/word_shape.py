import src.lojban_specific.phonological_inventory as inv

def word_shape(word):

    try:
        return ''.join((inv.char_type.get(char, char) for char in word))
    except:
        return ''