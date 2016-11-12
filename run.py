import math
import httplib2
import sqlite3
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
    search_db,
)

monkey.patch_all()

CLIENT_ID = '312115341730-c0rd7eo1u97h7c6r2qo0hva6ntiag5ki.apps.googleusercontent.com'
CLIENT_SECRET = 'H-7_uURyXKwTvegQBhcsMsE0'
SCOPE = ['profile', 'email']
# REDIRECT_URI = 'http://localhost:8080/oauth2callback'
REDIRECT_URI = 'http://ec2-52-5-94-6.compute-1.amazonaws.com:8080/oauth2callback'

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
maxPage = None

EntryPerPage = 10


@route('/favicon.ico', method='GET')
def get_favicon():
    return static_file('favicon.ico', root='static/')


@route('/static/<folder>/<filename>')
def send_file(folder, filename='index.html'):
    return static_file(filename, root='static/{}/'.format(folder))


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
                user=user,
            )

        word_count = get_word_count(search_string)
        search_string = get_first_word(search_string)

        # Fetch relevant URLs ordered by page rank
        global orderedURLS
        orderedURLS = search_db(db_conn=db_conn, word=search_string)

        if not orderedURLS:
            return template(
                'templates/empty',
                search_string=search_string,
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

        if email:
            update_keywords(
                search_history_map=search_history_map,
                email=email,
                data=word_count,
                search_string=search_string,
            )

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
