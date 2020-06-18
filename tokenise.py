import re
import json
import operator 
import nltk
from collections import Counter
from collections import defaultdict
from nltk.corpus import stopwords
import string
import vincent
import pandas
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
punctuation = list(string.punctuation)
#filtering out certain words
stop = stopwords.words('english') + punctuation + ['RT', 'via','“',"’",'…']

def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

fname = 'python.json'

dates_BLM = []
with open(fname, 'r') as f:
    for line in f:
        try:
            tweet = json.loads(line)
            terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
            if '#BLM' in terms_hash:
                dates_BLM.append(tweet['created_at'])
        except ValueError:
            pass

ones = [1]*len(dates_BLM)
idx = pandas.DatetimeIndex(dates_BLM)
ITAvWAL = pandas.Series(ones, index=idx)
 
per_minute = ITAvWAL.resample('1S').sum().fillna(0)

time_chart = vincent.Line(per_minute)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('time_chart.json')