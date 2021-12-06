import re
import json

import pymorphy2

from wiki_ru_wordnet import WikiWordnet
from nltk.stem.snowball import SnowballStemmer

morph = pymorphy2.MorphAnalyzer()
wiki_wordnet = WikiWordnet()

filename = 'bashim.json'
filename_synonyms = 'synonyms.txt'

with open(filename, encoding="utf-8") as f:
    document_json = json.load(f)

tokens = set()

for i in range(len(document_json)):
    words = document_json[i]['quote_text']
    tokens.update(words.split())


def append_value(dict_obj, key, value):
    if key in dict_obj:
        if not isinstance(dict_obj[key], list):
            dict_obj[key] = [dict_obj[key]]
        dict_obj[key].append(value)
    else:
        dict_obj[key] = value


# synonyms
with open(filename_synonyms, 'a', encoding='utf-8') as f:
    for i in list(tokens):
        syn = wiki_wordnet.get_synsets(i)
        if syn:
            list_get_words = syn[0].get_words()
            for j, word in enumerate(list_get_words):
                if len(list_get_words) != 1:
                    real_word = word.lemma().lower()
                    if j != 0:
                        f.write(f',{real_word}')
                    else:
                        f.write(f'\n{real_word}')

# stemmer and lemma
stemmer = SnowballStemmer("russian")
lem = pymorphy2.MorphAnalyzer()
dict_stem = {}
for word in list(tokens):
    # stem
    new_word = re.sub("[:|)|!|(|,|.|<|>|?|\"|\[|\]]", "", word).lower()
    stem_syn = stemmer.stem(new_word).lower()
    # lemma
    lemma = lem.parse(new_word)[0].normal_form
    if new_word != stem_syn:
        if stem_syn in dict_stem and new_word not in dict_stem[stem_syn]:
            append_value(dict_stem, stem_syn, new_word)
        else:
            dict_stem[f'{stem_syn}'] = new_word
    if new_word != lemma:
        if lemma in dict_stem and new_word not in dict_stem[lemma]:
            append_value(dict_stem, lemma, new_word)
        else:
            dict_stem[f'{lemma}'] = new_word


with open(filename_synonyms, 'a', encoding='utf-8') as f:
    for i in dict_stem:
        value = dict_stem[i]
        f.write(f'\n{i}')
        if isinstance(value, list):
            for j in value:
                f.write(f',{j}')
        elif isinstance(value, str):
            f.write(f',{value}')
