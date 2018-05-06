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

testcase1 = {
    # ["step_name", "request_type", "request_url", "request_data_type", "request_data", "expect_result", [{label:{"key":"value"}}]]
}

class TestEngine:
    def __init__(self):
        self.engine_list = []
        self.request_list = {}
        self.request_list["post"] = TestPostRequest
        self.request_list["put"] = TestPutRequest
        self.request_list["get"] = TestGetRequest
        self.request_list["delete"] = TestDeleteRequest
    def addcase(self, case):
        self.engine_list.append(case)
    def execute(self):
        for case in self.engine_list:
            self.docase(case)
    def docase(self, case):
        step_name = case[0]
        print step_name

        request_type = case[1]
        request_url = case[2]
        request_argument_type = case[3]
        request_data = case[4]
        expect_result = case[5]
        self.step_execute(step_name, request_type, request_url, request_argument_type, request_data, expect_result)

    def step_execute(self, step_name, request_url, request_type, request_data_type, request_data,expect_result):

        status, content = self.request_list[request_type](request_url) 

        if status == expect_result:
            print "\033[32;1m[SUCCESS] %s" % step_name
        
            #self.check_content(content)
        else:
            print "\033[31;1m[FAILED] %s" % step_name
    
    # key = [key1, key2, key3]
    def check_content(self, content, json_keys, json_value):
        result_json = json.loads(content)

        i = 0
        temp_json = result_json
        for jkey in json_keys:
            if jkey in temp_json:
                temp_json = temp_json[jkey]
                i = i + 1
            else:
                break
        if len(json_keys) == i and temp_json == json_value:
            return True
        else:
            return False

# data format  {'key1': 'value1', 'key2': 'value2'}
def TestGetRequest(url, data_type, data):
    if data == None:
        r = requests.get(url)
    else:
        if data_type == "path":
            r = requests.get(url, params=data)
        elif data_type == "body":
            r = requests.get(url, data=data)

    return r.status_code, r.content

def TestPostRequest(url, data_type, data):
    if data == None:
        r = requests.post(url)
    else:
        if data_type == "path":
            r = requests.post(url, params=data)
        elif data_type == "body":
            r = requests.post(url, data=data)

    return r.status_code, r.content

def TestPutRequest(url, data_type, data):
    r = requests.post(url)
    return r.status_code, r.content

def TestDeleteRequest(url, data_type, data):
    r = requests.post(url)
    return r.status_code, r.content

def ExpectResult():
    pass

def TestOauthRequest():
    r = requests.post(ADDRESS + "/oauth/token?grant_type=password&username=user&password=password", auth=HTTPBasicAuth('', ''))
    data = json.loads(r.content)
    print r.content
    r = requests.post(ADDRESS + "/oauth/token?grant_type=refresh_token&refresh_token=%s"%data[u'refresh_token'], auth=HTTPBasicAuth('', ''))
    print r.content
    return data[u'access_token']


if __name__ == '__main__':
    #print TestOauthRequest()
    te = TestEngine()
    #te.execute()
    print te.check_content('{"test1": {"test2": 1}}', ["test1", "test2"], 1)