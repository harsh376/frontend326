from bottle import (
    route,
    run,
    template,
    request,
    error,
)
from utils import get_word_count, update_keywords, get_top_20_keywords

keywords_map = {}


@route('/')
def home():
    if request.GET.save:
        search_string = request.GET.keywords.strip()
        word_count = get_word_count(search_string)
        update_keywords(keywords_map, word_count)

        return template(
            'templates/search',
            search_string=search_string,
            word_count=word_count,
        )
    else:
        top_20_keywords = get_top_20_keywords(keywords_map)
        return template(
            'templates/home',
            top_20_keywords=top_20_keywords,
        )


@error(404)
def mistake404():
    return 'Sorry, this page does not exist!'

run(host='0.0.0.0', port=8080)
