import requests

base_url = 'http://127.0.0.1:5000/'
# # base_url = 'https://exactmark.pythonanywhere.com/'
# add_user = 'add_single_user/'
# myobj = {'id': 'Orange', 'pw': 'OrangePw'}
#
# x = requests.get(base_url + add_user, params=myobj)
#
# print(x.text)

# dde8f3c8-f909-484c-83e6-a113b8535828


location_folder = 'put_location_image'
#
# # files = {'file': ('particles.jpg', open('particles.jpg', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
# # files = {'file': ('particles.jpg', open('particles.jpg', 'rb'), {'Expires': '0'})}
files = {'file': ('PXL_20210318_161905029.jpg', open('PXL_20210318_161905029.jpg', 'rb'), {'Expires': '0'})}
data = {'loc_id':'44','user_id':'Red',"session_key":'dde8f3c8-f909-484c-83e6-a113b8535828'}
x = requests.post(base_url + location_folder, files=files,data=data)
#
print(x.text)
