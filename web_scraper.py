import requests
import json
import nltk
from newsapi import NewsApiClient

#Init - using public API from newsapi.org
news = NewsApiClient(api_key = 'ff9c7139e58c42b0a5b823056d4d9392')

#list all US-based general news sources
sources = news.get_sources(category='general', language='en', country='us')['sources']
source_list = []
for s in sources:
    source_list.append(s['id'])
