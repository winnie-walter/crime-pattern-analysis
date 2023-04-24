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
new_data = new_data.drop(columns=['Human Trafficking','Child Stealing'], axis=1)


crime = ['Murder','Rape','Child Desertion','Unnatural Offence','Defilement']

for crime in crime:
    
    new_data[crime]=new_data[crime].astype(str)

for j in new_data:
 for i in range(len(new_data)):
    new_data[j][i]=new_data[j][i].replace(',', '')
crime = ['Murder','Rape','Child Desertion','Unnatural Offence','Defilement']
for crime in crime:
    
    new_data[crime]=new_data[crime].astype(float)
crime = ['Murder','Rape','Child Desertion','Unnatural Offence','Defilement']
for crime in crime:
    
    new_data[crime]=new_data[crime].astype(int)
crime = ['Murder','Rape','Child Desertion','Unnatural Offence','Defilement']
new_data['Total']=0
total = 0

new_data['Total'] = new_data['Murder']+new_data['Rape']+new_data['Child Desertion']+new_data['Unnatural Offence']+new_data['Defilement']

regions = [    'Arusha',    'Dar es Salaam',    'Dodoma',    'Geita',    'Iringa',    'Kagera',    'Katavi',    'Kigoma',    'Kilimanjaro',    'Lindi',    'Manyara',    'Mara',    'Mbeya',    'Morogoro',    'Mtwara',    'Mwanza',    'Njombe',    'Pemba North',    'Pemba South',    'Pwani',    'Rukwa',    'Ruvuma',    'Shinyanga',    'Simiyu',    'Singida',    'Songwe',    'Tabora',    'Tanga',    'Unguja North',    'Unguja South',    'Zanzibar Central/South']


        
#print(new_data['Police Region'])
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
data.insert(loc=data.columns.get_loc('STATE_UT')+2,column='YEAR', value='2016')
data = data.reset_index(drop=True).dropna()
data.columns = data.columns.str.replace(' ','_')
# print(data)
regions = [    'Arusha',    'Dar-es-Salaam',    'Dodoma',    'Geita',    'Iringa',    'Kagera',    'Katavi',    'Kigoma',    'Kilimanjaro',    'Lindi',    'Manyara',    'Mara',    'Mbeya',    'Morogoro',    'Mtwara',    'Mwanza',    'Njombe',    'Pemba North',    'Pemba South',    'Pwani',    'Rukwa',    'Ruvuma',    'Shinyanga',    'Simiyu',    'Singida',    'Songwe',    'Tabora',    'Tanga',    'Unguja North',    'Unguja South',    'Zanzibar Central/South']
regions = [ s.upper() for s in regions]

data = data[data['STATE_UT'].isin(regions)]

data.to_csv('fullsjsondata2016.csv',index=False)
data = data.to_dict(orient='records')

print(data)
with open('static\\assets\\data\\fulldata2016.json', 'w') as f:
    json.dump(data,f)
    
