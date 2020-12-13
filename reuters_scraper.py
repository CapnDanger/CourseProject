from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
import nltk
import re
import urllib
import time

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

#Adapted from MP2.1
def scrape_links(dir_url,driver):
    url_list = [] #for easier access later when obtaining content
    output_line = []
    base_url = "https://www.reuters.com"
    soup = get_js_soup(dir_url,driver)
    content = soup.find('div', class_ = 'column1 col col-10')
    with open('reuters_urls.csv', 'a+') as f:
        for link_holder in content.find_all('div', class_ = 'story-content'): #get list of all <div>
            output_line = []
            try:
                rel_link = link_holder.find('a')['href'] #get url
                url_list.append(base_url+rel_link)

                headline = link_holder.find('h3', class_ = 'story-title').string.strip()
                headline = headline.replace("'", "\\'") #add escape chars for quotes
                headline = headline.replace("\"", '\\' + '\"')
                headline = headline.replace(",", ";") #replace commas in headline with semicolon for CSV purposes
                publishDate = link_holder.find('span', class_ = 'timestamp').string.strip()

                output_line.append(publishDate)
                output_line.append(headline)
                output_line.append(base_url+rel_link)
                f.write(','.join(map(str, output_line)) + "\n")

            except:
                continue

    return url_list


def scrape_article(url):
    soup = get_js_soup(url, driver)
    body = soup.find_all('p', class_='Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x')
    txt = ''

    for p in body:
        try:
            txt += process_article(p.string)
        except:
            continue

    with open('reuters_body.txt', 'a+') as t:
        t.write(txt.replace("\n", '') + "\n")

#main scrape

reuters_links = []

with open('reuters_urls.csv', 'a+') as f:
    output_line = []
    output_line.append('publish_date')
    output_line.append('headline')
    output_line.append('url')
    f.write(','.join(map(str, output_line)) + "\n")

for i in range(1, 347):
    print('-'*20, 'Page ' + str(i), '-'*20)
    tgt_url = "https://www.reuters.com/news/archive/us-elections-2020?view=page&page={}&pageSize=10".format(i)
    reuters_links += scrape_links(tgt_url, driver)

print(str(len(reuters_links)), 'links scraped')

for i in range(len(reuters_links)):
    scrape_article(reuters_links[i])

driver.close()
