import json
import requests
from bs4 import BeautifulSoup

url  = "https://stockanalysis.com/stocks/"
res  = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")
res_json = json.loads(soup.find('script', type='application/json').contents[0])

# # dict_keys(['props', 'page', 'query', 'buildId', 'isFallback', 'gsp', 'scriptLoader'])
# print(res_json.keys())
# 
# # dict_keys(['pageProps', '__N_SSG'])
# print(res_json['props'].keys())
# 
# # dict_keys(['stocks'])
# print(res_json['props']['pageProps'].keys())
# 
# # dict_keys(['s', 'n', 'mcap', 'ind'])
# print(res_json['props']['pageProps']['stocks'][0].keys())

for t in res_json['props']['pageProps']['stocks']:
    print(t['s'])
