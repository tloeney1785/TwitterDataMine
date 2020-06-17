import re
import json
import operator 
import nltk
from collections import Counter
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
#  testing
# tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(preprocess(tweet))
# ['RT', '@marcobonzanini', ':', 'just', 'an', 'example', '!', ':D', 'http://example.com', '#NLP']

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
            # Create a list with all the terms
            terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
            # Update the counter
            count_all.update(terms_stop)
        except ValueError:
            pass
    # Print the first 5 most frequen
    print(count_all.most_common(5))

    # Count terms only once, equivalent to Document Frequency
# terms_single = set(terms_all)
# # Count hashtags only
# terms_hash = [term for term in preprocess(tweet['text']) 
#               if term.startswith('#')]
# # Count terms only (no hashtags, no mentions)
# terms_only = [term for term in preprocess(tweet['text']) 
#               if term not in stop and
#               not term.startswith(('#', '@'))] 
#               # mind the ((double brackets))
#               # startswith() takes a tuple (not a list) if 
#               # we pass a list of inputs