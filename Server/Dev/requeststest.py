import requests

url = 'http://127.0.0.1:5000/single_location/1'
myobj = {'somekey': 'somevalue',"yes":"no","tired":"me"}

x = requests.get(url, params=myobj)

print(x.text)

