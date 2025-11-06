import re
import numpy as np

def compensatory_lengthening(word, probability=1):
    """
    vowel lengthens and overwrites following consonant: atta -> aata
    """

    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer("[aeiou][b-df-hj-np-tv-z]", word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            span = match.span()
            word = word[:span[0] + 1] + word[span[0]] + word[span[1]:]
    
    return word

def rhotacism(word, probability=1):
    """
    s or z between vowels becomes an r: asa -> ara
    """

    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer('(?<=[aeiou])[sz](?=[aeiou])', word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            span = match.span()
            word = word[:span[0]] + 'r' + word[span[0] + 1:]

    return word

def metathesis(word, probability=1):
    """
    sounds flip position: asta -> atsa or asata -> atasa
    """

    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer('(?<=[b-df-hj-np-tv-z])[b-df-hj-np-tv-z]', word)] + [x for x in re.finditer('(?<=[b-df-hj-np-tv-z])[aeiou][b-df-hj-np-tv-z]', word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            span = match.span()
            if span[1] - span[0] == 1:
                word = word[:span[0] - 1] + word[span[0]] + word[span[0] - 1] + word[span[0] + 1:]
            else:
                word = word[:span[0] - 1] + word[span[0] + 1] + word[span[0]] + word[span[0] - 1] + word[span[0] + 2:] 

    return word

def haplology(word, probability=1):
    """
    removes sequential repetitions: abakakab -> abakab
    """

    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer('(\w{2})\\1', word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            span = match.span()
            word = word[:span[0]+2] + word[span[1]:]

    return word

def diphthongization(word, probability=1, weighted_options="aeiou"):
    """
    diphtongization of a vowel: atata -> atatae
    """

    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer('(?<![aeiou])([aeiou])(?![aeiou])', word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            span = match.span()
            new_vowel = np.random.choice(list(weighted_options.replace(word[span[0]], '')))
            if np.random.uniform(0, 1) < 0.5:
                word = word[:span[0]] + new_vowel + word[span[0]:]
            else:
                word = word[:span[0] + 1] + new_vowel + word[span[0+1]:]

    return word

def final_devoicing(word, probability=1):
    sound_map = {
        "b" : "p",
        "v" : "f",
        "d" : "t",
        "z" : "s",
        "j" : "ch",
        "g" : "k"
    }

    if np.random.uniform(0, 1) < probability:
        if word[-1] in sound_map.keys():
            word = word[:-1] + sound_map[word[-1]]

    return word

def intervocalic_voicing(word, probability=1):
    sound_map = {
        "p" : "b",
        "f" : "v",
        "t" : "d",
        "s" : "z",
        "ch" : "j",
        "k" : "g"
    }
    
    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer('(?<=[aeiou])(p|f|t|s|ch|k)(?=[aeiou])', word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            span = match.span()
            word = word[:span[0]] + sound_map[word[span[0]:span[1]]] + word[span[1]:]

    return word

def nasal_assimilation(word, probability=1):
    """
    nasalization of vowel before a nasal consonant: junp -> jump
    """
    sound_map = {
        "np" : "mp",
        "mt" : "nt"
    }

    if np.random.uniform(0, 1) < probability:
        for key, value in sound_map.items():
            word = word.replace(key, value)

    return word

def monophthongization(word, probability=1):
    """
    reduction of a diphthong to a monphthong: taek -> tak
    """
    if np.random.uniform(0, 1) < probability:
         matches = [x for x in re.finditer('(?<=[aeiou])([aeiou])', word)]
         if len(matches) > 0:
            match = np.random.choice(matches)
            span = match.span()
            if np.random.uniform(0, 1) > .5:
                word = word[:span[0]] + word[span[0] + 1:]
            else:
                word = word[:span[0] - 1] + word[span[0]:]

    return word

def gemination(word, probability=1):
    """
    duplicating of a consonant between two vowels: ata -> atta
    """
    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer('(?<=[aeiou])([b-df-hj-np-tv-z])(?=[aeiou])', word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            span = match.span()

            word = word[:span[1]] + word[span[0]:]

    return word

def degemination(word, probability=1):
    """
    reducing a doubled consonant to a single: atta -> ata
    """
    if np.random.uniform(0, 1) < probability:
        matches = [x for x in re.finditer('([b-df-hj-np-tv-z])\\1', word)]
        if len(matches) > 0:
            match = np.random.choice(matches)
            span = match.span()

            word = word[:span[0]] + word[span[0] + 1:]

    return word
