import sys
import json
import pdb
import re
from collections import defaultdict

class Tweet(object):
    def __init__(self, text):
        self.text = text

    @classmethod
    def from_json(self, json):
        return Tweet(json['text'])

    @classmethod
    def is_tweet(self, json):
        return json.has_key('text')

    def analyze_sentiment(self, sentiments):
        sum = 0
        unknown_words = []
        for word in self.text.split(' '):
            word = word.lower()
            word = re.sub(r'[^a-z]', '', word)
            if len(word) == 0:
                continue

            if sentiments.has_key(word):
                sum += sentiments[word]
            else:
                unknown_words.append(word)
        return sum, unknown_words

def parse_sentiments(afinnfile):
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    return scores

def parse_tweets(tweet_file):
    tweets = []
    for line in tweet_file:
        tweet_json = json.loads(line)
        if Tweet.is_tweet(tweet_json):
            tweet = Tweet.from_json(tweet_json)
            tweets.append(tweet)
    return tweets

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiments = parse_sentiments(sent_file)
    tweets = parse_tweets(tweet_file)

    new_words = defaultdict(list)
    for tweet in tweets:
        sentiment, unknown_words = tweet.analyze_sentiment(sentiments)
        for word in unknown_words:
            new_words[word].append(sentiment)

    for word, scores in new_words.items():
        average = float(sum(scores))/len(scores)
        print word, average

if __name__ == '__main__':
    main()
