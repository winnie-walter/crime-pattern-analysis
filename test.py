# import requests
# import re
# from bs4 import BeautifulSoup as bs
# import pandas as pd
# import nltk
# from nltk.tokenize import word_tokenize

# words = ['ubakaji', 'wizi','ujambazi','ujangili','utekaji','mauaji']
# data = {'Link':[], 'ubakaji':[], 'wizi':[], 'ujambazi':[], 'ujangili':[], 'utekaji':[], 'mauaji':[]}
# memory = []
# link_data = pd.read_csv('links.csv')
# for link in link_data['Link']:
    

#     data1 = requests.get(link).text
#     soup = bs(data1,'html.parser')
#     nltk.download('punkt')
#     s = soup.find('body')
    
#     f = word_tokenize(s.text)

#     i=0
#     while i<len(f):
#         for word in words:
#             if f[i] == word:
#                 memory.append(word)
#         i+=1
#     orginal__data = list(set(memory))

#     for org in words:
#         if org in orginal__data:
#             print('ACTIVE')
#             data[org].append(1)
#             data['Link'].append(link)
#         else:
#             print('LOWER')
#             data[org].append(0)
#             data['Link'].append(link)
            
            
# data['Link'] = list(set(data['Link']))
# pd_data = pd.DataFrame(data)
# pd_data.to_csv('maneno.csv',index=False)
    


 




import os
import pandas as pd
import json

csv_files = [file for file in os.listdir('static/assets/datasets') if file.endswith('.xlsx')]
dfs = []

# Loop through each CSV file and read it into a dataframe
for file in csv_files:
 df = pd.read_excel(os.path.join('static/assets/datasets', file))
 dfs.append(df)

# Concatenate all dataframes into a single dataframe
merged_df = pd.concat(dfs, ignore_index=True)
datas = merged_df.to_dict(orient='records')
merged_df.to_excel('static/assets/datasets/fulldata.xlsx')
with open('static/assets/datasets/fulldata.json', 'w') as g:
 json.dump(datas,g)