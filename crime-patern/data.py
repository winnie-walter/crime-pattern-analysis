import pandas as pd 
import json


import json
#import csv
import pandas as pd

location = 'crime.csv'
json_file = 'fulldata2016.json'

# with open (location, 'r') as f:
#     csv_reader =  csv.DictReader(f)
    
#     data = []
    
#     for row in csv_reader:
#         data.append(row)  

df = pd.read_csv('crime.csv')
df = pd.DataFrame(df)
new_data = df.dropna(axis=1,how='all')
new_data = new_data.drop(new_data.index[-1])

new_data.to_csv('fulldata2016.csv',index=False)

df = pd.read_csv('fulldata2016.csv')

mask = df['Police Region'].isin(['Temeke','Ilala','Kinondoni'])
columns = df.columns[1:]
df[columns]  = df[columns].apply(pd.to_numeric,errors="coerce")
#print(columns)
new_d = df[mask].sum().to_frame().T
new_d['Police Region'] = 'Dar-es-salaam'

df = pd.concat([df[-mask], new_d], ignore_index=True)
data = df.rename(columns={'Police Region':'STATE_UT','Total':'TOTAL_IPC_CRIMES'})

data.columns = data.columns.str.upper()
data['STATE_UT'] = data['STATE_UT'].str.upper()

data = data.sort_values('STATE_UT')
data.insert(loc=data.columns.get_loc('STATE_UT')+1,column='DISTRICT', value='TOTAL')
data = data.reset_index(drop=True).dropna()
data.columns = data.columns.str.replace(' ','_')
print(data)
data.to_csv('fulldata2016.csv',index=False)
data = data.to_dict(orient='records')

#print(data)
with open('static\\assets\\data\\fulldata2016.json', 'w') as f:
    json.dump(data,f)