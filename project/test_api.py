import requests
import json
import google.oauth2.credentials
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow


def get_request():
    """
    function get info request from file config.json
    """
    request = json.load(open('config.json'))
    return request


def get_authenticated_service():
    """
    function get token authenticate for using api
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return credentials.token


def get_response(token, uri, param, type, content):
    if type == 'get':
        r = requests.get(url=uri, params=param,
                         headers={'Authorization': 'Bearer %s' % token})
    elif type == 'post':
        r = requests.post(url=uri, params=param, data=content
                         headers={'Authorization': 'Bearer %s' % token})
    elif type == 'put':
        r = requests.put(url=uri, params=param,
                         headers={'Authorization': 'Bearer %s' % token})
    elif type == 'delete':
        r = requests.delete(url=uri, params=param,
                         headers={'Authorization': 'Bearer %s' % token})
    return r.json()


if __name__ == '__main__':
    CLIENT_SECRETS_FILE = "client_secret.json"
    SCOPES = 'https://www.googleapis.com/auth/youtube.force-ssl'

    request = get_request()
    client = get_authenticated_service()
    url = request['url'] + '/' + request['service_name']+'/'+request['service_version']+'/'+request['resources']
    response = get_response(client, url, request['params'], request['type'])
    print(response)
