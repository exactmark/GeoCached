import requests

base_url = 'http://127.0.0.1:5000/'
# # base_url = 'https://exactmark.pythonanywhere.com/'
# add_user = 'add_single_user/'
# myobj = {'id': 'Orange', 'pw': 'OrangePw'}
#
#
# print(x.text)

# dde8f3c8-f909-484c-83e6-a113b8535828
x = requests.get(base_url + '/get_location_list/')
print(x.text)

data = {'id':'0'}
x = requests.get(base_url + '/get_single_location/' ,params=data)
print(x.text)

path_qualifier = '/add_log_entry/'

data = {'loc_id': '1', 'user_id': 'Red', "session_key": 'dde8f3c8-f909-484c-83e6-a113b8535828',
        'text':'I am a log entry but not a third (this is a lie)'}
x = requests.post(base_url + path_qualifier, data=data)
#
print(x.text)

path_qualifier = '/get_log_entries/'

data = {'loc_id': '3', 'user_id': 'Red', "session_key": 'dde8f3c8-f909-484c-83e6-a113b8535828'}
x = requests.get(base_url + path_qualifier, params=data)
#
print(x.text)

