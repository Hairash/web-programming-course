import requests

x = requests.get('https://www.google.com')
# Make POST request with params

print(x.text)