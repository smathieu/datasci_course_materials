import sys
import json
import pdb
import re
from collections import defaultdict, Counter

class Tweet(object):
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags

    @classmethod
    def from_json(self, json):
        tags = json['entities']['hashtags']
        extracted_tags = []
        for tag in tags:
            extracted_tags.append(tag['text'])
        return Tweet(json['text'], extracted_tags)

    @classmethod
    def is_tweet(self, json):
        return json.has_key('text')

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

    hashtags = defaultdict(int)
    for tweet in tweets:
        for tag in tweet.tags:
            hashtags[tag] += 1

    answers = Counter(hashtags).most_common(10)
    for tag, num in answers:
        print tag, num

if __name__ == '__main__':
    main()

