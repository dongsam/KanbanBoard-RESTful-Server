#-*-coding: utf-8-*-
__author__ = 'dongsamb'
import json
import requests
import datetime



baseUrl = 'http://127.0.0.1:5000/'
headers = {'Content-Type': 'application/json'}

def createBoard(created_date=datetime.date.today().strftime('%d-%m-%y')):
    url = baseUrl + 'api/board'
    data = dict(created_date=created_date)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print response.status_code
    assert response.status_code == 201

# # Make a POST request to create an object in the database.
# data = dict(created_date=datetime.date.today().strftime('%d-%m-%y'))
# response = requests.post(url, data=json.dumps(data), headers=headers)
# print response.status_code
# # assert response.status_code == 201


def selectBoard():
    url = baseUrl + 'api/board'
    response = requests.get(url, headers=headers)
    print response.status_code
    assert response.status_code == 200
    print(response.json())


def insertList(board_id="1"):
    url = baseUrl + 'api/list'
    data = dict(board_id=board_id)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print response.status_code
    assert response.status_code == 201

def insertCard(list_id="1",title=""):
    url = baseUrl + 'api/card'
    data = dict(list_id=list_id, title=title)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print response.status_code
    assert response.status_code == 201


selectBoard()
insertList(2)
insertCard(1,u"테스트 test")


#delete test
# response = requests.delete(url + "/1", headers=headers)
# print response