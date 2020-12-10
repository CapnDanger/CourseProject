from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
#import requests_oauthlib
import json

#From MP2.1
#create a webdriver object and set options for headless browsing
# options = Options()
# options.headless = True
# driver = webdriver.Chrome('./chromedriver',options=options)

def scrape(url):
    with requests.Session() as req:
        with open('urls.csv', 'a+') as db:
            output_line = []
            output_line.append('id')
            output_line.append('publishDate')
            output_line.append('section')
            output_line.append('byline')
            output_line.append('headline')
            output_line.append('url')
            db.write(','.join(map(str, output_line)) + "\n")
            with open('body.txt', 'a+', encoding="utf-8") as f:
        #for i in range(1, 100, 100):
                r = req.get(url).json()
                for a in r['result']:
                    output_line = []
                    output_line.append(a['_id'])
                    output_line.append(a['firstPublishDate']) #FIXME: Truncate publish dates
                    output_line.append(a['section'])
                    output_line.append(a['byLine']) #FIXME: Truncate "..., CNN" from bylines
                    output_line.append(a['headline']) #FIXME: Add quotes around headline and/or escape commas
                    output_line.append(a['url'])
                    db.write(','.join(map(str, output_line)) + "\n")
                    f.write(a['body'] + "\n") #FIXME: figure out how to capture full articles, how to deal with the updating blogs

scrape("https://search.api.cnn.io/content?q=election&type=article&sort=newest&category=us,politics&size=10&from=1")
