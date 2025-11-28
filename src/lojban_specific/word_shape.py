import src.lojban_specific.phonological_inventory as inv

def word_shape(word):

    try:
        for char in word:
            if char in inv.C:
                word = word.replace(char, 'C')
            elif char in inv.A:
                word = word.replace(char, 'A')

        if "'" in word:
            word = word.replace("'", "")
    
        return word
    
    except:
        return ''