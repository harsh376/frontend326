import operator
from collections import OrderedDict
from nltk.tokenize import RegexpTokenizer

def parse_string(search_string):
    string_lower = search_string.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    result = tokenizer.tokenize(string_lower)
    return result


def get_word_count(search_string):
    result = OrderedDict()
    words = parse_string(search_string)
    for w in words:
        count = result.get(w, 0)
        result[w] = count + 1
    return result


def update_keywords(keywords_map, data):
    for key in data:
        old_val = keywords_map.get(key, 0)
        keywords_map[key] = old_val + data[key]
    return keywords_map


def get_top_20_keywords(keywords_map):
    sorted_keywords = sorted(
        keywords_map.items(),
        key=operator.itemgetter(1),
        reverse=True,
    )
    top_20_keywords = sorted_keywords[0:20]
    return OrderedDict(top_20_keywords)
