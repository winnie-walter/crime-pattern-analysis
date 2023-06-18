# import pandas as pd

# import json
# sem1 = pd.read_csv('fulljsondata2016.csv')

# sem2= pd.read_csv('fullsjsondata2015.csv')

# merge = pd.merge(sem1,sem2, how='outer')

# merge.to_csv('combine.csv')
# data = merge.to_dict(orient='records')

# with open('static\\assets\\data\\fullcombine.json', 'w') as f:
#     json.dump(data,f)
    
import datetime


date = datetime.datetime.now().year

date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
print(date)