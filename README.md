# Documentation

# Python Files

cnn_scraper.py: Used to scrape CNN articles. Accesses the publicly available CNN API.
fox_scraper.py: Used to scrape Fox News articles. Accesses the back-end API to scrape article information, then uses those links to access articles.
reuters_scraper.py: Used to scrape Reuters articles. Scrapes list of articles and then uses those links to access articles.
ibm_sentiment.py: Uses the IBM Watson Natural Language Understanding API to analyze the sentiment of each corpus of articles. Targets are set to analyze sentiment for keywords "Trump" and "Biden".

See inline comments for detailed descriptions of code functions.
Note that the scrapers take a long time to run (sometimes upwards of 1-2 hours), while the sentiment analysis takes ~20-30 minutes to run.

# Output Files
XXX_urls.csv: contains data on each corpus. All files contain the publish date, headline, url, and trump/biden sentiment scores. Depending on the source, may also include authors or category.
XXX_scores.csv: output of ibm_sentiment for each file. This can be manually copy/pasted to the respective XXX_urls file to populate those columns.
XXX_body.txt: output of XXX_scraper scripts. Each file contains one article per line, in the same order as the respective XXX_urls file.

# Other File
chromedriver: necessary for selenium package to operate the scraper

# API Documentation
The IBM Watson Natural Language Understanding API documentation can be found at https://cloud.ibm.com/apidocs/natural-language-understanding?code=python#sentiment

# Other attributions
Select portions of the scraper codes have been adapted from MP2.1. 

# Video Demonstration
https://mediaspace.illinois.edu/media/t/1_ksj5ytyq
