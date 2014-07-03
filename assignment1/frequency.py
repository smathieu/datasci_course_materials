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

    def words(self):
        words = []
        for word in self.text.split(' '):
            word = word.lower()
            word = re.sub(r'[^a-z]', '', word)
            if len(word) > 0:
                words.append(word)

        return words

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
    tweet_file = open(sys.argv[1])

    tweets = parse_tweets(tweet_file)

    words = defaultdict(int)
    for tweet in tweets:
        for word in tweet.words():
            words[word] += 1

    total = sum(words.values())

    for word, count in words.items():
        print "%s %f" %(word, float(count) / total)


if __name__ == '__main__':
    main()

