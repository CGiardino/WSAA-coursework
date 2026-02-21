import requests
import urllib.parse
from configs.config import api_keys

target_url = "http://andrewbeatty1.pythonanywhere.com/bookviewer.html"
html2pdf_api_key = api_keys["html2pdf"]
api_url = 'https://api.html2pdf.app/v1/generate'
params = {'html': target_url, 'apiKey': html2pdf_api_key}
parsed_params = urllib.parse.urlencode(params)
request_url = f'{api_url}?{parsed_params}'
response = requests.get(request_url)
print(response.status_code)
result = response.content

with open('data/book.pdf', 'wb') as f:
    f.write(result)
    