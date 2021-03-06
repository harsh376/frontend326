import math
import httplib2
import sqlite3
import enchant
import autocomplete
from gevent import monkey
from oauth2client.client import (
    flow_from_clientsecrets,
    OAuth2WebServerFlow,
)
from googleapiclient.discovery import build
from bottle import (
    app,
    route,
    run,
    template,
    request,
    error,
    static_file,
    redirect,
    response,
)
from beaker.middleware import SessionMiddleware
from utils import (
    get_word_count,
    update_keywords,
    get_history_table,
    get_first_word,
    get_all_words,
    search_db,
    eval_expr,
)

monkey.patch_all()
autocomplete.load()

CLIENT_ID = '312115341730-c0rd7eo1u97h7c6r2qo0hva6ntiag5ki.apps.googleusercontent.com'
CLIENT_SECRET = 'H-7_uURyXKwTvegQBhcsMsE0'
SCOPE = ['profile', 'email']
# REDIRECT_URI = 'http://localhost:8080/oauth2callback'
REDIRECT_URI = 'http://ec2-34-193-243-71.compute-1.amazonaws.com:8080/oauth2callback'

search_history_map = {}
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True,
}

app = SessionMiddleware(app(), session_opts)

# My glob vars
db_conn = None
ss = None
numrows = None
curr_row = None
orderedURLS = None
missingwords = None
maxPage = None
EntryPerPage = 5
ignored_words = [
            '', 'the', 'of', 'at', 'on', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
        ]
d = enchant.Dict("en_US")
suggestedsearch = None


@route('/favicon.ico', method='GET')
def get_favicon():
    return static_file('favicon.ico', root='static/')


@route('/static/<folder>/<filename>')
def send_file(folder, filename='index.html'):
    return static_file(filename, root='static/{}/'.format(folder))


@route('/autocomplete', method='GET')
def get_autocomplete_results():
    if request.GET.search_query:
        search_query = request.GET.search_query.strip()
        tup = tuple(search_query.split())

        if len(tup) < 2:
            return {'elements': ''}
        else:
            b = [str(i) for i in tup[:-1]]
            base = '+'.join(b)

            tup = tup[-2:]
            global autocomplete
            result = autocomplete.predict(*tup)
            result = sorted(result, key=lambda x: x[1])[::-1]
            result = [r[0] for r in result]
            result = result[:5]

            dom_list = []
            for sugg in result:
                s = base + '+' + sugg

                label = ' '.join(b + [sugg])

                dom = '<div class=\"autocomplete-sug\"><a href=\"/?keywords=' + s + '&save=search\">' + label + '</a></div>'
                dom_list.append(dom)

            res = ''.join(dom_list)
            return {'elements': res}


@route('/', method='POST')
def results():
    s = request.environ.get('beaker.session')
    user = s.get('user')
    email = user.get('email') if user else None

    up = request.forms.get('nav')
    global curr_row
    global currentPage

    if up == "nextPage":
        curr_row += EntryPerPage
        tempval = orderedURLS[curr_row:min(numrows, curr_row+EntryPerPage)]
        currentPage += 1
        result = tempval

    elif up == "prevPage":
        curr_row -= EntryPerPage
        currentPage -= 1
        tempval = orderedURLS[curr_row:curr_row+EntryPerPage]
        result = tempval
 
    else:
        currentPage = int(up)
        curr_row = (currentPage - 1)*EntryPerPage
        tempval = orderedURLS[curr_row:curr_row+EntryPerPage]
        result = tempval
 
    # range of pages
    if currentPage >= 10:
        begin = max(currentPage-8, 2)
        end = min(currentPage+1, maxPage)
    else:
        begin = 1
        end = min(maxPage, 10)

    #print ss, result
    return template(
        'templates/newresults',
        search_string=ss,
        user=user,
        result=result,
        currRow=curr_row,
        val=numrows,
        url=format(request.url),
        currentPage=currentPage,
        range=range(begin, end+1),
        missingwords=missingwords,
        suggestedsearch=suggestedsearch
    )


@route('/')
def home():
    # Fetching user
    s = request.environ.get('beaker.session')
    user = s.get('user')
    email = user.get('email') if user else None

    response.set_header(
        'Cache-Control',
        'no-cache, no-store, max-age=0, must-revalidate',
    )
    response.set_header('Pragma', 'no-cache')
    response.set_header('Expires', '0')

    if request.GET.save:
        search_string = request.GET.keywords.strip()
        if not search_string:
            return template(
                'templates/empty',
                search_string=search_string,
                suggestedsearch=None,
                user=user,
            )
        
        word_count = get_word_count(search_string) 

        value = eval_expr(search_string)
        if value:
            if email:
                update_keywords(
                search_history_map=search_history_map,
                email=email,
                data=word_count,
                search_string=search_string,
                ) 

            return template(
                'templates/calculator',
                search_string=search_string,
                user=user,
                value=value,
            )

        words = get_all_words(search_string)
        search_string = ' '.join(words)
        
        if email:
            update_keywords(
                search_history_map=search_history_map,
                email=email,
                data=word_count,
                search_string=search_string,
            ) 

        words = [i for i in words if i not in ignored_words]
        sug_words = [word for word in words]
        global suggestedsearch
        suggestedsearch = None
        changed_something = False
        for i,word in enumerate(words):
            if not d.check(word):
                suggested_word = d.suggest(word)[0]
                if not suggested_word or (suggested_word.lower() == word):
                    continue
                changed_something = True
                sug_words[i] = suggested_word

        if len(words) != 0:
            suggestedsearch = ' '.join(sug_words)

        if not changed_something:
            suggestedsearch = None

        # Fetch relevant URLs ordered by page rank
        global orderedURLS
        orderedURLS = None
        
        intersectionList = []

        global missingwords
        missingwords = []

        # get list of combined urls
        for word in words:
            wlist = search_db(db_conn=db_conn, word=word)
            if wlist is None or (len(wlist) == 0):
                missingwords = missingwords + [word]
            # Store all the links as well
            intersectionList = intersectionList + list(set(wlist) - set(intersectionList))
            if orderedURLS is not None: 
                orderedURLS = list(set(orderedURLS).intersection(wlist))
            else:
                orderedURLS = wlist
        
        if orderedURLS is None or (len(orderedURLS) == 0):
            orderedURLS = intersectionList

        # remove duplicate missing words
        missingwords = list(set(missingwords))
        if (len(missingwords) == 0):
            missingwords = None
        # resort based on page rank
        orderedURLS = sorted(orderedURLS, key=lambda x: x[2])
        intersectionList = sorted(intersectionList, key=lambda x: x[2])
        c = orderedURLS+intersectionList
        orderedURLS = sorted(set(c), key=lambda x: c.index(x))

        if not orderedURLS:
            return template(
                'templates/empty',
                search_string=search_string,
                suggestedsearch=suggestedsearch,
                user=user,
            )

        global numrows
        numrows = len(orderedURLS)
        global curr_row
        curr_row = 0
        global maxPage
        maxPage = int(math.ceil(float(numrows)/EntryPerPage))
        global currentPage
        currentPage = 1

        result = orderedURLS[0:min(numrows, EntryPerPage)]

        global ss
        ss = search_string

        # range of pages
        begin = 1
        end = min(maxPage, 10)

        return template(
            'templates/newresults',
            search_string=search_string,
            user=user,
            result=result,
            currRow=curr_row,
            val=numrows,
            url=format(request.url),
            currentPage=currentPage,
            range=range(begin,end+1),
            missingwords=missingwords,
            suggestedsearch=suggestedsearch,
        )
    else:
        history_table = {}
        if email:
            history_table = get_history_table(
                search_history_map=search_history_map,
                email=email,
            )

        return template(
            'templates/home',
            history_table=history_table,
            user=user,
        )


@route('/login/google', method='GET')
def login():
    s = request.environ.get('beaker.session')
    user = s.get('user')
    if user is None:
        flow = flow_from_clientsecrets(
            "credentials.json",
            scope=SCOPE,
            redirect_uri=REDIRECT_URI,
        )
        auth_uri = flow.step1_get_authorize_url()
        redirect(str(auth_uri))
    else:
        redirect('/')


@route('/oauth2callback')
def oauth2callback():
    code = request.query.get('code', '')
    flow = OAuth2WebServerFlow(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=SCOPE,
        redirect_uri=REDIRECT_URI,
    )
    credentials = flow.step2_exchange(code)
    http_auth = credentials.authorize(httplib2.Http())
    users_service = build('oauth2', 'v2', http=http_auth)
    user_profile = users_service.userinfo().get().execute()

    # Storing user in beaker session
    s = request.environ.get('beaker.session')
    s['user'] = user_profile
    s.save()

    redirect('/')


@route('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s['user'] = None
    s.save()
    redirect('/')


@error(404)
def mistake404(err):
    return '<html> \
                <h2> Sorry, this Page Does Not Exist! </h2> \
                <div> \
                    <a href="/"> <h3 class="results-search-for"> Return To Home Page </h3> </a> \
                </div>  \
            </html>'


if __name__ == '__main__':
    db_conn = sqlite3.connect('backend.db')
    run(server='gevent', app=app, host='0.0.0.0', port=8080)
