import tweepy
from tweepy import OAuthHandler

consumer_key = '7GyJCGrUdowLP5yJ0fJBZVW29'
consumer_secret = 'kChU2Xx8sbrEhW52vd5cHn7wVHHYhCoVbzXIxobZv1nI3cIRQ0'
access_token = '1272976469870833664-g1ngNVlJKsdqlpOInecrxAsYpKXgSb'
access_secret = '7rqs2YceDsjLsHNIB71ZUNX1TleRvij3w41y9Rb7kevh7'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)
