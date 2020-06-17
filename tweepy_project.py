import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json

consumer_key = '7GyJCGrUdowLP5yJ0fJBZVW29'
consumer_secret = 'kChU2Xx8sbrEhW52vd5cHn7wVHHYhCoVbzXIxobZv1nI3cIRQ0'
access_token = '1272976469870833664-g1ngNVlJKsdqlpOInecrxAsYpKXgSb'
access_secret = '7rqs2YceDsjLsHNIB71ZUNX1TleRvij3w41y9Rb7kevh7'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# def process_or_store(tweet):
#     print(json.dumps(tweet))
 
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#BLM'])

