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
# with open(fname, 'r') as f:
#     count_all = Counter()
#     for line in f:
#         try:
#             tweet = json.loads(line)
#             # Count hashtags only
#             terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')] 
#             count_all.update(terms_hash)
#             # terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
#         except ValueError:
#             pass
#     # Print the first 5 most frequen
#     print(count_all.most_common(5))

dates_BLM = []
# f is the file pointer to the JSON data set
with open(fname, 'r') as f:
    for line in f:
        try:
            tweet = json.loads(line)
            terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
            if '#BLM' in terms_hash:
                dates_BLM.append(tweet['created_at'])
        except ValueError:
            pass


# a list of "1" to count the hashtags
ones = [1]*len(dates_BLM)
# the index of the series
idx = pandas.DatetimeIndex(dates_BLM)
# the actual series (at series of 1s for the moment)
ITAvWAL = pandas.Series(ones, index=idx)
 
# Resampling / bucketing
per_minute = ITAvWAL.resample('10S').sum().fillna(0)

# word_freq = count_all.most_common(5)
# labels, freq = zip(*word_freq)
# data = {'data': freq, 'x': labels}
# bar = vincent.Bar(data, iter_idx='x')
# bar.to_json('term_freq.json')
time_chart = vincent.Line(per_minute)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('time_chart.json')