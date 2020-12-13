import requests
import json
import nltk

#CNN has an API that I was able to use, so there is no need to incorporate Beautiful Soup or Selenium.
def scrape(url):
    with requests.Session() as req:
        with open('cnn_urls.csv', 'w') as db:
            output_line = []
            output_line.append('id')
            output_line.append('publishDate')
            output_line.append('section')
            output_line.append('authors')
            output_line.append('headline')
            #output_line.append('sentences')
            output_line.append('url')
            db.write(','.join(map(str, output_line)) + "\n")
            with open('cnn_body.txt', 'w', encoding="utf-8") as f:
                for i in range(1, 7000, 100):
                    r = req.get(url.format(i)).json()
                    for a in r['result']:

                        # sent_list = nltk.sent_tokenize(a['body']) #tokenize into sentences
                        # for sent in sent_list: #Remove short sentences (4 words or fewer)
                        #     if sent.count(' ') <= 3:
                        #         sent_list.remove(sent)

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

                        #output_line.append(len(sent_list))

                        output_line.append(a['url'])
                        db.write(','.join(map(str, output_line)) + "\n")
                        f.write(a['body'].replace("\n", '') + "\n")

#main scrape
scrape("https://search.api.cnn.io/content?q=election&type=article&sort=newest&category=us,politics&size=100&from={}")
