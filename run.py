from bottle import (
    route,
    run,
    template,
    request,
    error,
)


@route('/')
def home():
    return template('templates/home')


@route('/search')
def search():
    if request.GET.save:
        search_term = request.GET.task.strip()
        return template('templates/search', search_term=search_term)
    else:
        return template('templates/home')


@error(404)
def mistake404():
    return 'Sorry, this page does not exist!'

run(host='0.0.0.0', port=8080)
