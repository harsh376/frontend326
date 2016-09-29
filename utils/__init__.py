from collections import OrderedDict


def parse_string(search_string):
    string_lower = search_string.lower()
    result = string_lower.split()
    return result


def get_word_count(search_string):
    result = OrderedDict()
    words = parse_string(search_string)
    for w in words:
        count = result.get(w, 0)
        result[w] = count + 1
    return result
