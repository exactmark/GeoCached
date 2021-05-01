import requests
import json

user_list = [{'id': 'Mark', 'pw': 'WeakPw'},
             {'id': 'Vishal', 'pw': 'WeakPw'},
             {'id': 'Lakshmi', 'pw': 'WeakPw'}]

base_url = 'http://127.0.0.1:5000/'
# base_url = 'https://exactmark.pythonanywhere.com/'


# add_user = 'add_single_user/'
# myobj = {'id': 'Orange', 'pw': 'OrangePw'}
#
#
# print(x.text)

# dde8f3c8-f909-484c-83e6-a113b8535828
# x = requests.get(base_url + '/get_location_list/')
# print(x.text)
#
# data = {'id':'0'}
# x = requests.get(base_url + '/get_single_location/' ,params=data)
# print(x.text)
#
# path_qualifier = '/add_log_entry/'
#
# data = {'loc_id': '1', 'user_id': 'Red', "session_key": 'dde8f3c8-f909-484c-83e6-a113b8535828',
#         'text':'I am a log entry but not a third (this is a lie)'}
# x = requests.post(base_url + path_qualifier, data=data)
# #
# print(x.text)
#
# path_qualifier = '/get_log_entries/'
#
# data = {'loc_id': '3', 'user_id': 'Red', "session_key": 'dde8f3c8-f909-484c-83e6-a113b8535828'}
# x = requests.get(base_url + path_qualifier, params=data)
# #
# print(x.text)

def add_session_key(new_data):
    target_url = base_url + "login"
    a_user = user_list[0]
    x = requests.post(target_url, a_user)
    new_data["session_key"] = json.loads(x.text)["session_key"]
    return new_data


data = {'id': "Mark", 'score': 10}
data = add_session_key(data)
url = base_url + "get_most_recent_log"
# x = requests.post(url,data)
x = requests.get(url, data)
print(x)
