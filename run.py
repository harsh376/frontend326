import httplib2
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
from collections import OrderedDict
from utils import (
    get_word_count,
    update_keywords,
    get_top_20_keywords,
)


CLIENT_ID = '312115341730-c0rd7eo1u97h7c6r2qo0hva6ntiag5ki.apps.googleusercontent.com'
CLIENT_SECRET = 'H-7_uURyXKwTvegQBhcsMsE0'
SCOPE = ['profile', 'email']
# REDIRECT_URI = 'http://localhost:8080/oauth2callback'
REDIRECT_URI = 'http://ec2-52-201-179-77.compute-1.amazonaws.com/oauth2callback'

search_history_map = {}
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True,
}

app = SessionMiddleware(app(), session_opts)


@route('/favicon.ico', method='GET')
def get_favicon():
    return static_file('favicon.ico', root='static/')


@route('/static/<folder>/<filename>')
def send_file(folder, filename='index.html'):
    return static_file(filename, root='static/{}/'.format(folder))


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
        word_count = get_word_count(search_string)

        if email:
            update_keywords(
                search_history_map=search_history_map,
                email=email,
                data=word_count,
            )

        return template(
            'templates/results',
            search_string=search_string,
            word_count=word_count,
            user=user,
        )
    else:
        top_20_keywords = OrderedDict()
        if email:
            top_20_keywords = get_top_20_keywords(
                search_history_map=search_history_map,
                email=email,
            )

        return template(
            'templates/home',
            top_20_keywords=top_20_keywords,
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
def mistake404():
    return 'Sorry, this page does not exist!'

if __name__ == '__main__':
    run(app=app, host='0.0.0.0', port=8080)
