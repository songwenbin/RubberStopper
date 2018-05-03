import requests 
import unittest
import json

from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

IP = 'http://192.168.1.172'
PORT = '8080'

ADDRESS = "%s:%s" % (IP, PORT)

URI = ""


class TestDeleteInterface():
    pass

class TestPostInterface():
    pass

class TestPutInterface():
    pass

class TestGetInterface():
    pass

class TestPatchInterface():
    pass

def TestPostRequest(url):
    pass

def ExpectResult():
    pass

def TestOauthRequest():
    r = requests.post(ADDRESS + "/oauth/token?grant_type=password&username=user&password=password", auth=HTTPBasicAuth('chiron-client', 'chiron'))
    data = json.loads(r.content)
    print r.content
    r = requests.post(ADDRESS + "/oauth/token?grant_type=refresh_token&refresh_token=%s"%data[u'refresh_token'], auth=HTTPBasicAuth('chiron-client', 'chiron'))
    print r.content
    return data[u'access_token']


if __name__ == '__main__':
    print TestOauthRequest()