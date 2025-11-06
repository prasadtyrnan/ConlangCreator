from googletrans import Translator
import asyncio
import unicodedata
import json
import numpy as np
import pandas as pd
import csv
import re

import deletions
import insertions
import mutations

function_mapper = {
    "syncope" : deletions.syncope,
    "apocope" : deletions.apocope,
    "aphaeresis" : deletions.aphaeresis,
    "prosthesis" : insertions.prosthesis,
    "anaptyxis" : insertions.anaptyxis,
    "excrescence" : insertions.excrescence,
    "paragoge" : insertions.paragoge,
    "compensatory_lengthening" : mutations.compensatory_lengthening,
    "rhotacism" : mutations.rhotacism,
    "metathesis" : mutations.metathesis,
    "haplology" : mutations.haplology,
    "diphthongization" : mutations.diphthongization,
    "final_devoicing" : mutations.final_devoicing,
    "intervocalic_voicing" : mutations.intervocalic_voicing,
    "nasal_assimilation" : mutations.nasal_assimilation,
    "monophthongization" : mutations.monophthongization,
    "gemination" : mutations.gemination,
    "degemination" : mutations.degemination
}

translator = Translator()
translator_loop = asyncio.new_event_loop()

def remove_accents(text):
    nfd_form = unicodedata.normalize('NFD', text)
    stripped_string = "".join(char for char in nfd_form if not unicodedata.combining(char))
    return stripped_string

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def translate(text, dest='es'):
    if translator_loop:
        output = translator_loop.run_until_complete(translator.translate(text, src='en', dest=dest))
    else:
        output = asyncio.run(translator.translate(text, src='en', dest=dest))

    if output.pronunciation != text:
        return remove_accents(output.pronunciation)

    return remove_accents(output.text)

def load_vocab_csv(filepath):
    vocab_mapper = {}
    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        _ = next(reader)

        for row in reader:
            vocab_mapper[row[0]] = row[1]

    return vocab_mapper

def save_vocab(filepath, vocab_dict):
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['base_word', 'permuted_word'])

        for key, value in vocab_dict.items():
            writer.writerow([key, value])


class Conlang():
    def __init__(self, conlang_name):
        config = json.load(open(f'saved_configurations/{conlang_name}/config.json', 'rb'))
        self.function_list = []
        for perm_name, perm_config in config['permutation_configurations'].items():
            base_function = function_mapper[perm_name]
            if "params" in perm_config.keys():
                paramed_function = (base_function, perm_config['params'])
            else:
                paramed_function = (base_function, {})

            self.function_list += [paramed_function]*perm_config['weight']
        
        self.enforce_permutation = config['enforce_permutation']
        self.min_permutations = config['permutation_minimum']
        self.max_permutations = config['permutation_maximum']
        self.language_code = config['base_language_code']
        self.vocab_dict = load_vocab_csv(f'saved_configurations/{conlang_name}/vocabulary.csv')
        self.name = conlang_name
        self.config = config

    def permute_word(self, word):
        num_permutations = np.random.randint(self.min_permutations, self.max_permutations + 1)
        completed_permutations = 0
        while completed_permutations < num_permutations:
            idx = np.random.randint(0, len(self.function_list))
            func = self.function_list[idx]
            # print(word, func[0].__name__)
            updated_word = func[0](word, **func[1])
            if self.enforce_permutation:
                if word != updated_word:
                    completed_permutations += 1
                    word = updated_word
            else:
                word = updated_word
                completed_permutations += 1

        return word
    
    def save_conlang_vocab(self):
        save_vocab(f"saved_configurations/{self.name}/vocabulary.csv", self.vocab_dict)
    
    def translate_text(self, text):
        translated_text = remove_punctuation(translate(text, self.language_code))
        words = translated_text.lower().split(" ")

        phrase_mapper = {}
        unique_words = list(set(words))
        new_words = {}

        for word in unique_words:
            if word in self.vocab_dict.keys():
                phrase_mapper[word] = self.vocab_dict[word]
            else:
                new_word = self.permute_word(word)
                phrase_mapper[word] = new_word
                self.vocab_dict[word] = new_word
                new_words[word] = new_word

        self.save_conlang_vocab()

        return " ".join([phrase_mapper[word] for word in words]), new_words
    
    def update_vocabulary(self, updates):
        for key, value in updates.items():
            self.vocab_dict[key] = value

        self.save_conlang_vocab()

    def get_vocabulary_table(self):
        return pd.read_csv(f"saved_configurations/{self.name}/vocabulary.csv")


"""test_conlang = Conlang('conlang_1')
print(test_conlang.translate_text("What's up?"))"""