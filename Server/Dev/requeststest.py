import requests

base_url = 'http://127.0.0.1:5000/'
# add_user = 'add_single_user/?id=Orange&pw=Bogus'
# myobj = {'id': 'Orange', 'password': 'OrangePw'}
#
# x = requests.get(base_url + add_user, params=myobj)
#
# print(x.text)


location_folder = 'put_location_image'

# files = {'file': ('particles.jpg', open('particles.jpg', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
# files = {'file': ('particles.jpg', open('particles.jpg', 'rb'), {'Expires': '0'})}
files = {'file': ('PXL_20210318_161905029.jpg', open('PXL_20210318_161905029.jpg', 'rb'), {'Expires': '0'})}
data = {'loc_id':'44','user_id':'Red'}
x = requests.post(base_url + location_folder, files=files,data=data)

print(x.text)
