import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json, operator,time,datetime
import nltk
import datetime
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re,csv
from collections import Counter
import string
#nltk.download()
from collections import defaultdict
import pprint

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
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

# General Dataset TimeSeries
df=pd.read_csv('streamind_data_sentiment12.csv')
#print df['sentiscore'].head(5)
df1=pd.concat([df['timestamp'],df['sentiscore']],axis =1)

#print df1.head(5)

with open('dataset.csv','a') as f:
	df1.to_csv(f,header=None,index = False,encoding='utf-8')

# Mirai and ddos Dataset TimeSeries

#df=pd.read_csv('streamind_data_sentiment11.csv')

f2=open('datasetddos.csv','a') 
f=open('datasetmirai.csv','a')
for index,row in df.iterrows():
	try:
		tok = preprocess(row['text'], True)
	except:
		pass	
	if 'mirai' in tok or '#mirai' in tok:
		#print True
		writer = csv.writer(f)
		writer.writerow([row['timestamp'],row['sentiscore']])
	if 'ddos' in tok or '#ddos' in tok:
		#print False
		writer = csv.writer(f2)
		writer.writerow([row['timestamp'],row['sentiscore']])	
	

print 'Finished'




