from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
import nltk
import re
import urllib
import time
import csv

#create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver',options=options)

#helper functions from MP2.1
#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,driver):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html, "lxml") #beautiful soup object to be used for parsing html content
    return soup

#tidies extracted text
def process_article(article):
    article = article.encode('ascii',errors='ignore').decode('utf-8')       #removes non-ascii characters
    article = re.sub('\s+',' ',article)       #repalces repeated whitespace characters with single space
    return article

''' More tidying
Sometimes the text extracted HTML webpage may contain javascript code and some style elements.
This function removes script and style tags from HTML so that extracted text does not contain them.
'''
def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup

#I was able to find a backend API and scrape it for the list of links
def scrape_links(url):
    url_list = [] #for easier access later when obtaining content
    with requests.Session() as req:
        with open('fox_urls.csv', 'r') as db:
            output_line = []
            output_line.append('publishDate')
            output_line.append('category')
            output_line.append('headline')
            output_line.append('url')
            output_line.append('sentences')
            #db.write(','.join(map(str, output_line)) + "\n")
            for i in range(6106, 8000, 100):
                r = req.get(url.format(i)).json()
                for a in r:
                    output_line = []

                    publishDate = a['publicationDate'][:10]
                    output_line.append(publishDate)

                    output_line.append(a['category']['name'])

                    headline = a['title'] #Add quotes around headline and escape comma characters
                    headline = headline.replace("'", "\\'") #add escape chars for quotes
                    headline = headline.replace("\"", '\\' + '\"')
                    headline = headline.replace(",", ";") #replace commas in headline with semicolon for CSV purposes
                    output_line.append(headline)

                    article_link = 'https://www.foxnews.com' + a['url']
                    output_line.append(article_link)
                    url_list.append(article_link)

                    output_line.append('0') #will be manually updated with sentences

                    #db.write(','.join(map(str, output_line)) + "\n")
    return url_list

def scrape_article(url):

    soup = get_js_soup(url, driver)
    body = soup.find('div', class_ = 'article-body')
    txt = remove_script(body).find_all('p')
    article_text = ''
    for i in txt:
        if not(str(i).startswith('<p data-')): #remove video captions and spam links
            filter = re.compile('<.*?>')
            clean = re.sub(filter, '', str(i)) #remove HTML Tags
            if not(clean.isupper()): #filter out spam - all caps links to other articles
                article_text += clean + ' '
    article_text = process_article(article_text)

    #tokenize article into sentences
    sent_list = nltk.sent_tokenize(article_text)
    for sent in sent_list: #Remove short sentences (4 words or fewer)
        if sent.count(' ') <= 3:
            sent_list.remove(sent)

    ct = len(sent_list) #number of sentences

    with open('fox_body.txt', 'a+') as t:
        for sent in sent_list:
            t.write(sent + "\n")

    with open('sent_counts.csv', 'a+') as c:
        c.write(str(ct) + "\n")


#main scrape

fox_links = scrape_links("https://www.foxnews.com/api/article-search?isTag=true&searchSelected=fox-news%2Fpolitics%2F2020-presidential-election&size=100&offset={}")
print(len(fox_links))

for i in range(len(fox_links)):
    scrape_article(fox_links[i])

driver.close()
#print(fox_links[0])