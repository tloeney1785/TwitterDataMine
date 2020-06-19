import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import time

consumer_key = '7GyJCGrUdowLP5yJ0fJBZVW29'
consumer_secret = 'kChU2Xx8sbrEhW52vd5cHn7wVHHYhCoVbzXIxobZv1nI3cIRQ0'
access_token = '1272976469870833664-g1ngNVlJKsdqlpOInecrxAsYpKXgSb'
access_secret = '7rqs2YceDsjLsHNIB71ZUNX1TleRvij3w41y9Rb7kevh7'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

class MyListener(StreamListener):

    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open('python.json', 'a')
        super(MyListener, self).__init__()

    def on_data(self, data):

        if (time.time() - self.start_time) < self.limit:
            self.saveFile.write(data)
            self.saveFile.write('\n')
            return True
        else:
            self.saveFile.close()
            return False
        # try:
        #     with open('python.json', 'a') as f:
        #         f.write(data)
        #         return True
        # except BaseException as e:
        #     print("Error on_data: %s" % str(e))
        # return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, listener=MyListener(time_limit=60))
twitter_stream.filter(track=['#BLM'], is_async=True)
