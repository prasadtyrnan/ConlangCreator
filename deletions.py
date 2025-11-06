import re
import numpy as np

def syncope(word, probability=1):
    """
    deletion of interior vowels: atata -> atta
    """
    if len(word) <= 2:
        return word
    
    matches = [x for x in re.finditer("(?<=[b-df-hj-np-tv-z])([aeiou]){1,2}(?=[b-df-hj-np-tv-z])", word)][::-1]
    
    for match in matches:
        if np.random.uniform(0, 1) < probability:
            span = match.span()
            word = word[:span[0]] + word[span[1]:]
    
    return word

def apocope(word, probability=1):
    """
    deletion of the end of the word: atata -> atat
    """
    if len(word) <= 2:
        return word
    
    if np.random.uniform(0, 1) < probability:
        word = word[:-1]

    return word

def aphaeresis(word, probability=1, vowel_probability=1):
    """
    deletion of initial sound, biased toward vowels: atata -> tata
    """
    if len(word) <= 2:
        return word
    
    roll = np.random.uniform(0, 1)
    if word[0] in 'aeiou':
        if roll < vowel_probability:
            word = word[1:]
    else:
        if roll < probability:
            word = word[1:]

    return word