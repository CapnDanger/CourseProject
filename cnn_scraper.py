#from bs4 import BeautifulSoup
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import requests
import json
import nltk

# def phrase(text):
#     phrase_list = []
#     sent_list = nltk.sent_tokenize(text) #tokenize text into sentences
#     for sent in sent_list: #split each sentence into
#         ph = sent.split(', ')
#         phrase_list.append(ph)
#     print(phrase_list)

def scrape(url):
    with requests.Session() as req:
        with open('urls.csv', 'w') as db:
            output_line = []
            output_line.append('id')
            output_line.append('publishDate')
            output_line.append('section')
            output_line.append('authors')
            output_line.append('headline')
            output_line.append('sentences')
            output_line.append('url')
            db.write(','.join(map(str, output_line)) + "\n")
            with open('body.txt', 'w', encoding="utf-8") as f:
                for i in range(1, 7000, 100):
                    r = req.get(url.format(i)).json()
                    for a in r['result']:

                        sent_list = nltk.sent_tokenize(a['body']) #tokenize into sentences
                        for sent in sent_list: #Remove short sentences (4 words or fewer)
                            if sent.count(' ') <= 3:
                                sent_list.remove(sent)

                        output_line = []
                        output_line.append(a['_id'])

                        publishDate = a['firstPublishDate'][:10]
                        output_line.append(publishDate)

                        output_line.append(a['section'])

                        #Most Bylines are formatted "By John Smith and Jane Doe, CNN"
                        byline = a['contributors']

                        authors = ' and '.join(map(str, byline))

                        output_line.append(authors)

                        headline = a['headline'] #Add quotes around headline and escape comma characters
                        headline = headline.replace("'", "\\'") #add escape chars for quotes
                        headline = headline.replace("\"", '\\' + '\"')
                        headline = headline.replace(",", ";") #replace commas in headline with semicolon for CSV purposes
                        output_line.append(headline)

                        output_line.append(len(sent_list))

                        output_line.append(a['url'])
                        db.write(','.join(map(str, output_line)) + "\n")
                        for sent in sent_list:
                            f.write(sent + "\n")


scrape("https://search.api.cnn.io/content?q=election&type=article&sort=newest&category=us,politics&size=100&from={}")
