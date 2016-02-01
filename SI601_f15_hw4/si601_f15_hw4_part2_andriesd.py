#!/usr/bin/env python

# Initial code for SI 601 F15 Hoemwork 4 Part 2

import oauth2 as oauth
import json, pydot
import re

# Twitter API documentation
# https://dev.twitter.com/overview/documentation

# Get access tokens from https://dev.twitter.com/oauth/overview/application-owner-access-tokens
consumer_key = 'eQOh7YAOvDurQbPOJapY6Afqj'
consumer_secret = '9KyWC5nIAbt59Z3iYjpFRUCOd6JF2qVw91d1UXxdpRNcONPzk9'
access_token = '2250647112-kerPftjEAuM0pDAIZI7fDzQXZn72NWoIPRgiFQn'
access_secret = 'sfSxC1Z69y9n57XAfqweJ8tPiaZPZNrU0tGxNLSPD32OV'

consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
token = oauth.Token(key=access_token, secret=access_secret)
client = oauth.Client(consumer, token)

# Get up to 200 tweets on your own home timeline
# Doc: https://dev.twitter.com/rest/reference/get/statuses/home_timeline
header, response = client.request('https://api.twitter.com/1.1/statuses/home_timeline.json?count=200', method="GET")

# print response

############################################################################
# add more code below to
# 1. load the response JSON string into a Python data structure
# 2. a graph in the DOT language using pydot such that if there is a tweet from
# user A, and the tweet mentions users B, C, D, then the directed edges A->B, A->C,
# A->D are added to the graph. Note that self-mentions should not count. 
# The results should be saved in a file like twitter_example_output.dot.
############################################################################

tweets = json.loads(response)
graph = pydot.Dot(graph_type='digraph')

tweet_pairs = set()
for tweet in tweets:
    tweet_text = tweet['text']
    mentioned = re.findall(r'@([a-zA-Z0-9_]+)', tweet_text)
    tweeter = tweet['user']['screen_name']
    # print tweeter
    # print tweet_text
    if len(mentioned) == 0:
        continue
    else:
        for mention in mentioned:
            if tweeter == mention:
                continue
            else:
                tweet_pairs.add((tweeter, mention))

for tweet in tweet_pairs:
    # print tweet[0], tweet[1]
    edge = pydot.Edge(tweet[0], tweet[1])
    graph.add_edge(edge)

graph.write('twitter_output_andriesd.dot')
graph.write_pdf('twitter_output_andriesd.pdf')
