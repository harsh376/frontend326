from bottle import (
    route,
    run,
    template,
    request,
    error,
)
from utils import get_word_count


@route('/')
def home():
    if request.GET.save:
        search_string = request.GET.keywords.strip()
        word_count = get_word_count(search_string)
        return template(
            'templates/search',
            search_string=search_string,
            word_count=word_count,
        )
    else:
        return template('templates/home')


@error(404)
def mistake404():
    return 'Sorry, this page does not exist!'

run(host='0.0.0.0', port=8080)
