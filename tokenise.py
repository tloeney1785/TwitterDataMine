import re
import json
import operator 
import nltk
from collections import Counter
from collections import defaultdict
from nltk.corpus import stopwords
import string
 
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

with open("python.json", 'r') as f:
    count_all = Counter()
    for line in f:
        try:
            tweet = json.loads(line)
        except ValueError:
            pass

fname = 'python.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        try:
            tweet = json.loads(line)
            # Count hashtags only
            terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')] 
            count_all.update(terms_hash)
            # terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
        except ValueError:
            pass
    # Print the first 5 most frequen
    print(count_all.most_common(5))

