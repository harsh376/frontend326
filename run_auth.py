from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from bottle import (
    route,
    run,
    template,
    request,
    error,
    static_file,
)
from utils import get_word_count, update_keywords, get_top_20_keywords

@route('/', 'GET')
def home():
    flow = flow_from_clientsecrets("client_secrets.json", 
                                    scope='https://www.googleapis.com/auth/plus.mehttp://www.googleapis.com/auth/userinfo.email', 
                                    redirect_uri="http://localhost:8080/redirect")
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))
    
@route('/redirect')
def redirect_page():
    code = request.query.get('code', '')
    flow = OAuth2WebserverFlow( client_id=CLIENT_ID, 
                                client_secrets=CLIENT_SECRET, 
                                scope=SCOPE, 
                                redirect_uri=REDIRECT_URI)
    credentials = flow.step2_exchange(code)
    token = credentials.id_token('sub')
    
run(host='0.0.0.0', port=8080)