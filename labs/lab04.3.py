import requests
import urllib.parse
from configs.config import api_keys
import json

github_api_key = api_keys["github_aprivateone"]
api_url = 'https://api.github.com/repos/CGiardino/aprivateone'
response = requests.get(api_url, auth = ('token', github_api_key))
print(response.status_code)
result = response.json()

with open('data/aprivateone.json', 'w') as f:
    json.dump(result, f, indent=4)
