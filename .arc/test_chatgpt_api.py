import requests

api_key = 'your_openai_api_key'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

data = {
    "prompt": "translate English to French: Hello, how are you?",
    "model": "text-davinci-003",
    "temperature": 0.5
}

response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
print(response.json())
