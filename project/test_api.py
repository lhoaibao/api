import requests
import json
import google.oauth2.credentials
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
from requests_toolbelt.utils import dump


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


def get_response(token, request):
    method = {
        "get": lambda url, params, body: requests.get(url=url, params=params,
                         headers={'Authorization': 'Bearer %s' % token}),

        "post": lambda url, params, body: requests.post(url=url, params=params, json=body,
                         headers={'Authorization': 'Bearer %s' % token}),
         "put": lambda url, params, body: requests.put(url=url, params=params, json=body,

                         headers={'Authorization': 'Bearer %s' % token}),
        "delete": lambda url, params, body: requests.delete(url=url, params=params,
                         headers={'Authorization': 'Bearer %s' % token}),
    }
    func = method.get(request["type"], lambda url, params: exit("invalid method"))
    try:
        response = func(request['url'] + '/' + request['resources'], request["params"], request["body"])
    except json.decoder.JSONDecodeError:
        print("json file is wrong")
        return
    return response.text


def main():
    try:
        request = get_request()
    except json.decoder.JSONDecodeError:
        print("json file is wrong")
        return
    client = get_authenticated_service()
    response = get_response(client, request)
    with open('response.txt', 'wb') as f:
        f.write(response.encode())


if __name__ == '__main__':
    CLIENT_SECRETS_FILE = "client_secret.json"
    SCOPES = 'https://www.googleapis.com/auth/youtube.force-ssl'
    main()
