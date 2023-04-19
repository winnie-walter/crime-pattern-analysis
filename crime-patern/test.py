import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

words = ['ubakaji', 'wizi','ujambazi','ujangili','utekaji','mauaji']
data = {'Link':[], 'ubakaji':[], 'wizi':[], 'ujambazi':[], 'ujangili':[], 'utekaji':[], 'mauaji':[]}
memory = []
link_data = pd.read_csv('links.csv')
for link in link_data['Link']:
    

    data1 = requests.get(link).text
    soup = bs(data1,'html.parser')
    nltk.download('punkt')
    s = soup.find('body')
    
    f = word_tokenize(s.text)

    i=0
    while i<len(f):
        for word in words:
            if f[i] == word:
                memory.append(word)
        i+=1
    orginal__data = list(set(memory))

    for org in words:
        if org in orginal__data:
            print('ACTIVE')
            data[org].append(1)
            data['Link'].append(link)
        else:
            print('LOWER')
            data[org].append(0)
            data['Link'].append(link)
            
            
data['Link'] = list(set(data['Link']))
pd_data = pd.DataFrame(data)
pd_data.to_csv('maneno.csv',index=False)
    


 








