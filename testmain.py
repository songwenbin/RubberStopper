# -*- coding: utf-8 -*-
import requests
import unittest
import json
import jinja2

from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import testcase
IP = 'http://192.168.1.102'
PORT = '8888'

ADDRESS = "%s:%s" % (IP, PORT)
URI = ""

data = {}
testcase1 = []
    # ["step_name", "request_type", "request_url", "request_data_type", "request_data", "expect_result", [{label:{"key":"value"}}]]
    # ["step_name", "request_type", "request_url", "request_data", "expect_result", "data_save"]
    # request_data:{"path":"value","param":"value"}
    # data_save:{"key":[test1,test2,test3],"key":[test4,test5,test6]}
    # expect_result:{"key":[[test1,test2,test3],excpet_content],"key2":[[test4,test5,test6],excpet_content_2]}
    # data_save{"key1":[test1,test2,test3],"key2":[test4,test5,test6]}


class TestEngine:
    def __init__(self):
        headers_data = TestOauthRequest()
        authorization = headers_data[u'token_type'] + " " + headers_data[u'access_token']
        headers = {
            'content-type': "application/json",
            'tenant': "tenant_test",
            'authorization': authorization,
        }
        self.headers = headers
        # self.request_list["post"] = TestPostRequest
        # self.request_list["put"] = TestPutRequest
        # self.request_list["get"] = TestGetRequest
        # self.request_list["delete"] = TestDeleteRequest
        self.engine_list = []
        self.request_list = {}
        self.response_data = {}

    def addcase(self, case):
        # self.engine_list.append(case)
        self.engine_list=case
    def execute(self):
        # for index,value in enumerate(self.engine_list):
        #     self.docase(value)
        self.docase(self.engine_list)
    def docase(self, case):
        step_name = case[0]
        print step_name
        request_type = case[1]
        request_url = case[2]
        # request_argument_type = case[3]
        request_data = case[3]
        expect_result = case[4]
        data_save = case[5]
        self.step_execute(step_name, request_type, request_url, request_data, expect_result,
                          data_save)

    def step_execute(self, step_name, request_type, request_url, request_data, expect_result,
                     data_save):
        # status, content = self.request_list[request_type](request_url)
        responseData = TestRequest(request_type, request_url, request_data, self.headers)
        content = json.loads(responseData.content)
        if responseData.status_code != 200:
            error = content[u'error'].encode('utf-8')
            print "\033[31;1m[FAILED] %s" % step_name + "请求失败，错误信息为：" + str(responseData.status_code) + "," + error
        elif content[u'result'] == expect_result:
            print "\033[32;1m[SUCCESS] %s" % step_name
            # self.check_content(content)
            SaveData(data_save, content)
            print(data)
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
# data_sava {'key':[test1,test2,test3],'key2':[test1,test2,test3]}
# 根据data_save的格式讲数据存入data中
def SaveData(data_save, responseData):
    for key in data_save:
        result = responseData
        i = 0
        for key1 in data_save[key]:
            if key1 in result:
                result = result[key1]
                i = i + 1
            if i == len(data_save[key]):
                data[key] = result


def TestRequest(type, url, reuest_data, headers):
    body = None
    params = None
    if "params" in reuest_data:
        params = reuest_data["params"]
    if "body" in reuest_data:
        body = reuest_data["body"]
    print(ADDRESS + url)
    print(body)
    print(params)
    if params == None and body == None:
        r = requests.request(type, ADDRESS + url, headers=headers)
    elif params != None and body != None:
        r = requests.request(type, ADDRESS + url, params=params, data=body, headers=headers)
    elif params != None and body == None:
        r = requests.request(type, ADDRESS + url, params=params, headers=headers)
    elif params == None and body != None:
        r = requests.request(type, ADDRESS + url, headers=headers,data=body)
    return r;


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


# 获取token信息
def TestOauthRequest():
    r = requests.post(ADDRESS + "/oauth/token?grant_type=password&username=user&password=password",
                      auth=HTTPBasicAuth('chiron-client', 'chiron'))
    token_data = json.loads(r.content)
    print r.content
    r = requests.post(ADDRESS + "/oauth/token?grant_type=refresh_token&refresh_token=%s" % token_data[u'refresh_token'],
                      auth=HTTPBasicAuth('', ''))
    return token_data
if __name__ == '__main__':
    # print TestOauthRequest()
    print(ADDRESS)
    # print(TestOauthRequest())
    te = TestEngine()
    testpaperContent = "{\r\n\t\"author\": \"俞瑶\",\r\n\t\"belongToCourseId\": \"1\",\r\n\t\"belongToCourseName\": \"课程1\",\r\n\t\"code\": \"42d0000s2047\",\r\n\t\"name\": \"俞瑶创建的第23张新试卷\",\r\n\t\"testPaperStruct\": {\r\n\t\t\"questionTypeStruct\": [{\r\n\t\t\t\"name\": \"单选题\",\r\n\t\t\t\"no\": \"一\",\r\n\t\t\t\"questionInPaper\": [{\r\n\t\t\t\t\t\"no\": \"1\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 1.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"2\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\":2.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"3\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 3.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"4\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"5\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 5.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"6\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 6.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"7\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 7.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"8\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 8.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"9\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 9.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"10\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 10.0\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"11\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.5\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"12\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.5\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"13\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.5\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"14\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.5\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"15\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.5\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"16\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.5\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"17\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.5\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"18\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\":4.5\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"19\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.5\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t\"no\": \"20\",\r\n\t\t\t\t\t\"questionId\": \"0768fa286a7347f89cb1f467e765db4e\",\r\n\t\t\t\t\t\"score\": 4.5\r\n\t\t\t\t}\r\n\t\t\t],\r\n\t\t\t\"score\": 100.0\r\n\t\t}],\r\n\t\t\"totalScore\": 100.0\r\n\t},\r\n\t\"totalScore\": 100.0,\r\n\t\"type\": \"期中考试\",\r\n\t\"usedCount\": \"10\"\r\n}"
    case1 = ["添加组卷", "POST", "/testpapers/smart", {"body": testpaperContent}, 0, {"testpaperId": ["data", "id"]}]
    # case2 = ["获取试卷详情", "GET", "/testpapers/" + str(testmain.data.get("testpaperId")), {}, 0, {"result": ["result"]}]
    case2 = ["获取试卷详情", "GET", "/testpapers/"+str(data.get("testpaperId")), {}, 0, {"result": ["result"]}]
    cases=[case1,case2]
    for index,value in enumerate(cases):
        te.addcase(value)
        te.execute()

    print te.check_content('{"test1": {"test2": 1}}', ["test1", "test2"], 1)
