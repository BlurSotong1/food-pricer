import requests

url = 'http://127.0.0.1:5000/ntuc/'
data = {'query': 'chicken'}
response = requests.post(url, json=data)
print(response)
print(response.json())