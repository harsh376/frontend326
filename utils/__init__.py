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


def word_to_wordid(cursor, search_string):
    cursor.execute("""SELECT * FROM lexicon WHERE word='%s';""" %(search_string))
    wordid = cursor.fetchone()
    if wordid is None:
        return None
    return wordid[0]

def doc_id_from_word_id(cursor, wordid):
    cursor.execute("""SELECT doc_id FROM inverted_index WHERE word_id='%s';""" %(wordid))
    tempval = cursor.fetchall()
    docids = [i[0] for i in tempval]
    return docids

def page_ranks_from_doc_id(cursor, docids):
    sql="select * from page_ranks where doc_id in ({seq})".format(seq=','.join(['?']*len(docids)))
    cursor.execute(sql, docids)
    tempval = cursor.fetchall()
    orderedRanks = sorted(tempval, key = lambda element : element[1])
    tempval = [i[0] for i in orderedRanks]
    tempval.reverse()
    return tempval

def urls_of_pages(cursor, pages):
    #sql_query = 'SELECT name FROM studens WHERE id in (' + ','.join(map(str, pages)) + ')'
    #print sql_query  
    sql="select title,url from doc_index where id in ({seq})".format(seq=','.join(['?']*len(pages)))
    #print sql
    cursor.execute(sql, pages)
    pages = cursor.fetchall()
    return [(str(i[0]),str(i[1])) for i in pages]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
