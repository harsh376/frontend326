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


def get_updated_mappings(word_count_mapping, data):
    """
    >>> word_count_mapping = {}
    >>> data = {'a': 1, 'b': 2}

    # When mappings are empty
    >>> word_count_mapping = get_updated_mappings(word_count_mapping, data)
    >>> word_count_mapping
    {'a': 1, 'b': 2}

    # When mappings are not empty
    >>> word_count_mapping = get_updated_mappings(word_count_mapping, data)
    >>> word_count_mapping
    {'a': 2, 'b': 4}
    """
    for key in data:
        old_val = word_count_mapping.get(key, 0)
        word_count_mapping[key] = old_val + data[key]
    return word_count_mapping


def update_keywords(search_history_map, email, data):
    """
    >>> search_history_map = {}
    >>> email = 'a@email.com'
    >>> data = {'a': 1, 'b': 2}
    >>> new_mappings = update_keywords(search_history_map, email, data)
    >>> new_mappings
    {'a@email.com': {'a': 1, 'b': 2}}

    >>> data = {'a': 1}
    >>> update_keywords(new_mappings, email, data)
    {'a@email.com': {'a': 2, 'b': 2}}
    """
    user_entry = search_history_map.get(email)
    if not user_entry:
        search_history_map[email] = get_updated_mappings({}, data)
    else:
        search_history_map[email] = get_updated_mappings(user_entry, data)
    return search_history_map


def get_top_20_keywords(search_history_map, email):
    """
    >>> search_history_map = {}
    >>> email = 'a@email.com'
    >>> get_top_20_keywords(search_history_map, email)
    OrderedDict()

    >>> search_history_map = {'b@email.com': {'a': 1, 'b': 2}}
    >>> email = 'a@email.com'
    >>> get_top_20_keywords(search_history_map, email)
    OrderedDict()

    >>> search_history_map = {'a@email.com': {'a': 1}}
    >>> email = 'a@email.com'
    >>> get_top_20_keywords(search_history_map, email)
    OrderedDict([('a', 1)])
    """

    keywords_map = search_history_map.get(email, {})
    sorted_keywords = sorted(
        keywords_map.items(),
        key=operator.itemgetter(1),
        reverse=True,
    )
    top_20_keywords = sorted_keywords[0:20]
    return OrderedDict(top_20_keywords)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
