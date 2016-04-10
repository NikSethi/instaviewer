try:
    import json
except ImportError:
    import simplejson as json

import twitter
from flask import Flask, request, render_template, session
import urllib
from app import app

ACCESS_TOKEN = '880929978-V3Vfb6qx93d9V2zJXHerYJJxFSxwjRouI4R77nMy'
ACCESS_SECRET = 'c9CbCbDUGktS2AMUfqTLMwf95Pu15HbMmiWZq9KTk8XoQ'
CONSUMER_KEY = 'Sb9KbtQoGRrI1yyi9z6D7fGTh'
CONSUMER_SECRET = 'RGSTd9jJhegi59AuxqNklIZSocPnQugb2OO5IT2JK7g6CilJ5Z'

api = twitter.Api(consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN,
                    access_token_secret=ACCESS_SECRET)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
@app.route('/index.html', methods=['POST'])
def index_post():
    text = request.form['text']
    processed_text = text.upper()
    values = {'q': text}
    data = urllib.urlencode(values) + '%20%3A)'
    # data = data + '&lang=en&result_type=recent'
    data = data.encode('utf8')

    iterator = api.GetSearch(data)
    iterator = (result.AsDict() for result in iterator)

    tweetList = []
    for tweet in iterator:
        string = tweet['text'].encode('utf8')
        datum = urllib.urlencode({"text": string})
        u = urllib.urlopen("http://text-processing.com/api/sentiment/", datum)
        sentimentResponse = json.loads(u.read())
        # print sentimentResponse['label']
        tweet['label'] = sentimentResponse["label"]
        if tweet['label'] == 'pos':
            tweetList.append(tweet)
        # print "potato",tweet



    return render_template('index.html', text=processed_text, iterator= tweetList, url=data)


