import re
import numpy as np

def prosthesis(word, probability=1, weighted_options='aeiou'):
    """
    insertion of initial vowel sound: tata -> atata
    """
    if word[0] in 'aeiou':
        return word

    if np.random.uniform(0, 1) < probability:
        word = np.random.choice(list(weighted_options)) + word

    return word

def anaptyxis(word, probability=1, weighted_options='aeiou'):
    """
    insertion of vowel between consonants: ata -> atata
    """
    if len(word) <= 1:
        return word

    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer("[b-df-hj-np-tv-z]", word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            vowel = np.random.choice(list(weighted_options))
            span = match.span()
            if span[0] + 1 < len(word) and word[span[0] + 1] in 'bcdfghjklmnpqrstvwxyz':
                word = word[:span[0] + 1] + vowel + word[span[0] + 1:]
            else:
                word = word[:span[0] + 1] + vowel + word[span[0]:]

    return word

def excrescence(word, probability=1, weighted_options='bcdfghjklmnpqrstvwxyz'):
    """
    insertion of consonant between other consonants: atta -> atmta
    """
    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer("[b-df-hj-np-tv-z]{2}", word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            letter = np.random.choice(list(weighted_options))
            span = match.span()
            word = word[:span[0] + 1] + letter + word[span[0] + 1:]

    return word

def paragoge(word, probability=1, weighted_options='aaaaabcdeeeeefghiiiiijklmnooooopqrstuuuuuvwxyz'):
    """
    insertion of an extra letter at the end: atat -> atata
    """
    if np.random.uniform(0, 1) < probability:
        letter = np.random.choice(list(weighted_options))
        word = word + letter

    return word