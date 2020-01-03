from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import oauth2client
from apiclient.discovery import build
import httplib2
import base64

CLIENTSECRETS_LOCATION = 'client_secret_496021465715-3eu6kui6ehktq31k3kl1j9m7v5f4imsn.apps.googleusercontent.com.json'
REDIRECT_URI = 'http://localhost:8080/oauth2callback'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

def exchange_code(authorization_code):
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    flow.redirect_uri = REDIRECT_URI
    try:
      credentials = flow.step2_exchange(authorization_code)
      return credentials
    except:
        print("something went wrong")


def get_authorization_url(email_address):
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    flow.params['access_type'] = 'offline'
    flow.params['approval_prompt'] = 'force'
    flow.params['user_id'] = email_address
    return flow.step1_get_authorize_url(REDIRECT_URI)

def get_refresh_token(authorization_code):
  credentials = exchange_code(authorization_code)
  return credentials.refresh_token
  
def watch(gmail):
    request = {
      'labelIds': ['INBOX'],
      'topicName': '<topic>'
    }
    print(gmail.users().watch(userId='me', body=request).execute())

def show_history(gmail, history_id):
    print(gmail.users().history().list(userId='me',startHistoryId=history_id).execute())

def get_message(gmail, message_id):
    return gmail.users().messages().get(userId='me', id=message_id).execute()

#refresh_token = '<refresh>'
#client_id = '<id>'
#client_secret = '<secret>'
#
#credentials = oauth2client.client.GoogleCredentials(None,client_id,client_secret,
#                                      refresh_token,None,"https://accounts.google.com/o/oauth2/token", None)
#http = credentials.authorize(httplib2.Http())
#credentials.refresh(http)
#gmail = build('gmail', 'v1', credentials=credentials)

# CALL FUNCTIONS

get_authorization_url("g0xchu@gmail.com")


code = input("code: ")

get_refresh_token(code)
