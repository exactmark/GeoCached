import requests

url = 'http://127.0.0.1:5000/add_single_user/?id=Orange&pw=Bogus'
myobj = {'id':'Orange', 'password':'OrangePw'}

x = requests.get(url, params=myobj)

print(x.text)

