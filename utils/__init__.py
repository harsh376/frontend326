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


def get_first_word(search_string):
    words = parse_string(search_string)
    return words[0]


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


def join_lists(list1, list2):
    """
    >>> list1= []
    >>> list2 = ['a', 'b', 'c', 'b']
    >>> list1 = join_lists(list1, list2)
    >>> list1
    ['a', 'b', 'c']

    >>> list2 = ['b', 'd', 'e']
    >>> list1 = join_lists(list1, list2)
    >>> list1
    ['a', 'b', 'c', 'd', 'e']
    """
    combined_list = list1 + list2
    seen = set()
    seen_add = seen.add
    result = [x for x in combined_list if not (x in seen or seen_add(x))]
    return result


def update_keywords(search_history_map, email, data, search_string):
    """
    >>> search_history_map = {}
    >>> email = 'a@email.com'
    >>> data = {'a': 1, 'b': 2}
    >>> search_string = 'A b'
    >>> new_mappings = update_keywords(search_history_map, email, data, search_string)
    >>> new_mappings
    {'a@email.com': {'word_count_map': {'a': 1, 'b': 2}, 'recent_searches': ['a', 'b']}}

    >>> data = {'a': 1}
    >>> update_keywords(new_mappings, email, data, search_string)
    {'a@email.com': {'word_count_map': {'a': 2, 'b': 2}, 'recent_searches': ['a', 'b']}}
    """

    user_entry = search_history_map.get(email)
    search_string_list = parse_string(search_string)

    if not user_entry:
        search_history_map[email] = {
            'word_count_map': get_updated_mappings({}, data),
            'recent_searches': search_string_list,
        }
    else:
        old_word_count_map = search_history_map[email]['word_count_map']
        old_recent_searches = search_history_map[email]['recent_searches']
        search_history_map[email] = {
            'word_count_map': get_updated_mappings(old_word_count_map, data),
            'recent_searches': join_lists(search_string_list, old_recent_searches)
        }
    return search_history_map


def get_user_data(search_history_map, email):
    """
    >>> search_history_map = {}
    >>> email = 'a@email.com'
    >>> get_user_data(search_history_map, email)
    {}

    >>> data_map = {'a': 1, 'b': 2}
    >>> search_history_map = {'b@email.com': {'word_count_map': data_map, 'recent_searches': ['a', 'b']}}
    >>> email = 'a@email.com'
    >>> get_user_data(search_history_map, email)
    {}

    >>> search_history_map = {'a@email.com': {'word_count_map': data_map, 'recent_searches': ['a', 'b']}}
    >>> email = 'a@email.com'
    >>> get_user_data(search_history_map, email)
    {'word_count_map': {'a': 1, 'b': 2}, 'recent_searches': ['a', 'b']}
    """

    user_history = search_history_map.get(email, {})
    return user_history


def get_history_table(search_history_map, email):
    user_data = get_user_data(search_history_map, email)
    word_count_map = user_data.get('word_count_map', {})
    recent_searches = user_data.get('recent_searches', [])

    result = OrderedDict()
    limit = 10
    num_results = limit if len(recent_searches) > limit else len(recent_searches)
    for i in range(num_results):
        item = recent_searches[i]
        result[item] = word_count_map[item]
    return result


def search_db(db_conn, word):
    cursor = db_conn.cursor()
    cursor.execute(
        """
        SELECT DISTINCT
            doc_index.title,
            doc_index.url,
            doc_index.id,
            page_ranks.rank
        FROM lexicon, doc_index, inverted_index, page_ranks
        WHERE
            lexicon.id = inverted_index.word_id AND
            inverted_index.doc_id = doc_index.id AND
            inverted_index.doc_id = page_ranks.doc_id
            AND lexicon.word = ?
        ORDER BY page_ranks.rank
        """,
        (word,),
    )
    result = cursor.fetchall()
    return result


def get_snippets(db_conn):
    cursor = db_conn.cursor()
    cursor.execute(
        """
        SELECT inverted_index.doc_id, snippets.text
        FROM inverted_index, snippets
        WHERE
            inverted_index.snippet_id = snippets.id
        """
    )
    result = cursor.fetchall()
    docid_snippet = {}
    for r in result:
        doc_id, snippet = r[0], r[1]
        temp = docid_snippet.get(doc_id)
        if temp:
            docid_snippet[doc_id].append(snippet)
        else:
            docid_snippet[doc_id] = [snippet]
    return docid_snippet

if __name__ == "__main__":
    import doctest
    doctest.testmod()
