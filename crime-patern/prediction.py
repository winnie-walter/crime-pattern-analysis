import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from prophet import Prophet     #facebook prophet package
import mpld3
def predictfun():
   
    data_prophet_df_final = pd.read_csv('actualdata2.csv')
    #print(data_prophet_df_final)

    filename="static/assets/data/predictinputjsondata.json"
    data_prophet_df_final.to_json(filename,orient='records')
    
    print(data_prophet_df_final)
    #instantiating prophet object
    model = Prophet()
    model.fit(data_prophet_df_final)

    future = model.make_future_dataframe(periods=365)  #periods = no. of days for prediction

    forecast = model.predict(future)

    forecast_ouptut=forecast[['ds','trend','yhat_lower','yhat_upper','yhat']]

    filename="static/assets/data/predictoutjsondata.json"
    forecast_ouptut.to_json(filename,orient='records')

    #visualizing future results
    figure = model.plot(forecast, xlabel='Date', ylabel='Crime Rate')
    
    print(forecast)
    # figure.savefig('static/assets/images/predictionresult.png')


    # #expected trend in the future
    figure3 = model.plot_components(forecast)

    # figure3.savefig('static/assets/images/predictiontrend.png')

    # print(forecast_ouptut)

