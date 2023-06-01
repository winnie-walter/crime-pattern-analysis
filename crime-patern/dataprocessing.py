import pandas as pd 
import json


import json
#import csv
import pandas as pd
import random

# Generate a random integer between 0 and 9


location = 'crime.csv'
json_file = 'fulldata2016.json'

# with open (location, 'r') as f:
#     csv_reader =  csv.DictReader(f)
    
#     data = []
    
#     for row in csv_reader:
#         data.append(row)  
import pandas as pd
import os
path = "C:\\Users\\Winnie Walter\\Documents\\crime data\\crime 2018.xlsx"
folder_path = 'crime_data'
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]
# print(csv_files)
# df_list = []
# for file in csv_files:
    #print(file)
# df = pd.read_excel(os.path.join(folder_path, file))

def preprocessings(path,year):
    df = pd.read_excel(path)
    df = pd.DataFrame(df)

    df.columns = df.columns.str.title()
    print(df.columns)
    new_data = df.dropna(axis=1,how='all')
    
    # print(new_data.head())
    new_data = new_data.drop(new_data.index[-1])

    #     new_data = new_data.drop(columns=['Human Trafficking','Child Stealing'], axis=1)


    crime = ['Police Region','Murder','Rape','Child Desertion','Unnatural Offense','Diflement']
    drop = []
    for i in new_data.columns:
        if  i not in crime:
            drop.append(i)
    new_data = new_data.drop(columns=drop,axis=1)  
   
    # for crime in crime:
        
    #     new_data[crime]=new_data[crime].astype(str)
    crime = ['Murder','Rape','Child Desertion','Unnatural Offense','Diflement']
    for j in new_data:
        for i in range(len(new_data)):
            new_data[j][i]=new_data[j][i]

        crime = ['Murder','Rape','Child Desertion','Unnatural Offense','Diflement']
        for crime in crime:
            
            new_data[crime]=new_data[crime].astype(float)

    # print(new_data.head())
    crime = ['Murder','Rape','Child Desertion','Unnatural Offense','Diflement']
    for j in new_data:
        for i in range(len(new_data)):
            new_data[j][i]=new_data[j][i]
            
            new_data[crime]=new_data[crime].astype(int)
            new_data['Total']=0
            #total = 0
            for k in new_data.columns[1:]:
                if k not in crime:
                    pass
                else:

                 new_data['Total'] = new_data['Total'] + new_data[k]
        # crime = ['Murder','Rape','Child Desertion','Unnatural Offence','Defilement']
    
  
   
    
    
    regions = [    'Arusha',    'Dar es Salaam',    'Dodoma',    'Geita',    'Iringa',    'Kagera',    'Katavi',    'Kigoma',    'Kilimanjaro',    'Lindi',    'Manyara',    'Mara',    'Mbeya',    'Morogoro',    'Mtwara',    'Mwanza',    'Njombe',    'Pemba North',    'Pemba South',    'Pwani',    'Rukwa',    'Ruvuma',    'Shinyanga',    'Simiyu',    'Singida',    'Songwe',    'Tabora',    'Tanga',    'Unguja North',    'Unguja South',    'Zanzibar Central/South']


    #     num = random.randint(0, 100) 
    #     #print(new_data['Police Region'])
    #     #new_data.to_csv(f'{num}.csv',index=False)

        

    #     # df = pd.read_csv('2016.csv')
    #     df = new_data
    dar = ['Temeke','Ilala','Kinondoni']
    mask = new_data['Police Region'].isin(['Temeke','Ilala','Kinondoni'])

    # for i in mask:
    #     if i == True:
    #         print(i)
    columns = new_data.columns[1:]

    new_data[columns]  = new_data[columns].apply(pd.to_numeric,errors="coerce")
    
    new_d = new_data[mask].sum().to_frame().T
    
    new_d['Police Region'] = 'Dar-es-salaam'
    #print(new_d) 
    df = pd.concat([new_data[-mask], new_d], ignore_index=True)

    #print(df.head())
    data = df.rename(columns={'Police Region':'STATE_UT','Total':'TOTAL_IPC_CRIMES'})
    # print(data.head()) 
    data.columns = data.columns.str.upper()
    data['STATE_UT'] = data['STATE_UT'].str.upper()
    
    data = data.sort_values('STATE_UT')
    data.insert(loc=data.columns.get_loc('STATE_UT')+1,column='DISTRICT', value='TOTAL')
    data.insert(loc=data.columns.get_loc('STATE_UT')+2,column='YEAR', value=year)
    data = data.reset_index(drop=True).dropna()
    data.columns = data.columns

    regions = [    'Arusha',    'Dar-es-Salaam',    'Dodoma',    'Geita',    'Iringa',    'Kagera',    'Katavi',    'Kigoma',    'Kilimanjaro',    'Lindi',    'Manyara',    'Mara',    'Mbeya',    'Morogoro',    'Mtwara',    'Mwanza',    'Njombe',    'Pemba North',    'Pemba South',    'Pwani',    'Rukwa',    'Ruvuma',    'Shinyanga',    'Simiyu',    'Singida',    'Songwe',    'Tabora',    'Tanga',    'Unguja North',    'Unguja South',    'Zanzibar Central/South']
    regions = [ s.upper() for s in regions]

    data = data[data['STATE_UT'].isin(regions)]


    # print(data.head())
        
    
    data.to_excel('processed_data/'+str(year)+'.xlsx',index=False)
    
    data = data.to_dict(orient='records')
    
    return data
    # with open('static\\assets\\data\\fulldata2016.json', 'w') as f:
    #  json.dump(data,f)
# path = 'C:\\Users\\Winnie Walter\\Documents\\crime data\\crime2016.xlsx'
dt = preprocessings(path,2020)

# print(dt)

