import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

authenticator = IAMAuthenticator('5iBHhYb2Ni_ezxGWzivM_2sA1eCDjV-jDeEC8CNN9j8z')
nlu = NaturalLanguageUnderstandingV1(version='2020-08-01', authenticator=authenticator)

nlu.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/c3a1ef64-02ae-47bb-ace5-2c8716994177/v1/analyze?version=2019-07-12')

trump_scores = []
biden_scores = []

with open('fox_body.txt', 'r', encoding="utf-8") as f:
    corpus = f.readlines()

print(len(corpus))

for d in corpus:
    targets = []
    d = d.strip()
    trump = 0
    biden = 0

    if ('Trump ' in d):
        targets.append('Trump')
    if ('Biden ' in d):
        targets.append('Biden')

    if (len(targets) > 0):
        response = nlu.analyze(
            text = d,
            features = Features(sentiment = SentimentOptions(targets = targets))).get_result()

        res = response["sentiment"]["targets"]

        for i in res:
            if (i["text"] == "Trump"):
                trump = i["score"]
            elif (i["text"] == "Biden"):
                biden = i["score"]

    trump_scores.append(trump)
    biden_scores.append(biden)
    if(len(trump_scores) % 100 == 0):
        print(len(trump_scores))

with open('fox_scores.csv', 'w') as o:
    for i in range(len(trump_scores)):
        output_line = []
        output_line.append(trump_scores[i])
        output_line.append(biden_scores[i])
        o.write(','.join(map(str, output_line)) + "\n")
