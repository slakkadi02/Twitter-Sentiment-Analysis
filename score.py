from subprocess import Popen, PIPE, STDOUT
import numpy as np
import pandas as pd

import json,sys

df = pd.DataFrame()
with open('2016-10-13.json') as rb:
    data = rb.readlines()
results = []
for line in data:
    line = json.loads(line)
    temp = {}
    temp['tweet_id'] = line.get('id', None)
    #temp['user_id'] = line['user']['id']
    temp['timestamp'] = line.get('created_at',None)
    temp['text'] = line.get('text',None)
    results.append(temp)

# print results[0]
df = pd.DataFrame.from_dict(results)    
df['sentiscore'] = np.zeros(len(df.index))

def get_sentiment(text):
    p = Popen(['java', '-jar', './SentiStrength.jar', 'sentidata', './data/', 'text', text], stdout=PIPE, stderr=STDOUT, cwd=SENTISTRENGTHDIR)
    #print(p.stdout)
    for line in p.stdout:
        #print(line)
        return map(int, line.split())

SENTISTRENGTHDIR = './SentiStrength/'
for i in df.index:
    #print get_sentiment(df.text.ix[i]), df.text.ix[i]
    #print str(i) + '/' + str(len(df.index)) + ' >',
    try:
        df.sentiscore.ix[i] = np.mean(get_sentiment(df.text.ix[i]))
    #print("value", df.sentiscore.ix[i])
    except:
        pass
    #print df.sentiscore.ix[i]
df.to_csv('streamind_data_sentiment13.csv', encoding='utf-8')



