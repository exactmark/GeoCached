import requests

url = 'http://127.0.0.1:5000/add_user'
myobj = {'id':'Orange', 'password':'OrangePw'}

x = requests.get(url, params=myobj)

print(x.text)

