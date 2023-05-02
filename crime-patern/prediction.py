# import the necessary libraries
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import random
import threading
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# load the crime data
crime_data = pd.read_excel('static/assets//fulldata/fulldata.xlsx')

num = random.randint(0,1000)
def predict_range(state,year,year2,crime):
    

    # convert the STATE_UT column to one-hot encoded binary columns
    encoder = OneHotEncoder(sparse=False)
    state_encoded = encoder.fit_transform(crime_data[['STATE_UT']])
    state_labels = encoder.categories_[0]

    state_df = pd.DataFrame(state_encoded, columns=[f'STATE_UT_{label}' for label in state_labels])

    # combine the one-hot encoded state columns with the rest of the data
    X = pd.concat([state_df, crime_data[['YEAR']]], axis=1)
    y = crime_data[crime]

    # create a linear regression model and fit it on the data
    model = LinearRegression()
    model.fit(X, y)


    # take input values for state and year
        # state = 'DODOMA'
        # year = 2021
    years = []
    crime_rates = []
    for i in range(year,year2+1):
    # create a dataframe with the input values
        input_data = pd.DataFrame({'STATE_UT': [state], 'YEAR': [i]})
        input_state_encoded = encoder.transform(input_data[['STATE_UT']])
        input_state_df = pd.DataFrame(input_state_encoded, columns=[f'STATE_UT_{label}' for label in state_labels])
        input_data = pd.concat([input_state_df, input_data[['YEAR']]], axis=1)

        # predict the total IPC crimes for the input values
        predicted_ipc_crimes = model.predict(input_data)

        # print the predicted total IPC crimes
        # print(i)
        # print('Predicted Total IPC Crimes:', abs(predicted_ipc_crimes))
        
        years.append(int(i))
        crime_rates.append(abs(predicted_ipc_crimes[0]))
        
    fig, ax = plt.subplots()
    # plot the line graph of crime rate against year
    ax.bar(years, crime_rates)
    ax.set_xticks(years)  # set the x-axis ticks to show all the years
    ax.set_xlabel('Year')
    ax.set_ylabel('Crime Rate')
    ax.set_title(f'Crime Rate for {state} from {year} to {year2}')
    path = f'static/assets/predict/image{num}.png'
    fig.savefig(path)
    #plt.show()
    
    return path

def predict(state,year,crime):
    

    # convert the STATE_UT column to one-hot encoded binary columns
    encoder = OneHotEncoder(sparse=False)
    state_encoded = encoder.fit_transform(crime_data[['STATE_UT']])
    state_labels = encoder.categories_[0]

    state_df = pd.DataFrame(state_encoded, columns=[f'STATE_UT_{label}' for label in state_labels])

    # combine the one-hot encoded state columns with the rest of the data
    X = pd.concat([state_df, crime_data[['YEAR']]], axis=1)
    y = crime_data[crime]

    # create a linear regression model and fit it on the data
    model = LinearRegression()
    model.fit(X, y)


    # take input values for state and year
        # state = 'DODOMA'
        # year = 2021
    years = []
    crime_rates = []
    
    # create a dataframe with the input values
    input_data = pd.DataFrame({'STATE_UT': [state], 'YEAR': [year]})
    input_state_encoded = encoder.transform(input_data[['STATE_UT']])
    input_state_df = pd.DataFrame(input_state_encoded, columns=[f'STATE_UT_{label}' for label in state_labels])
    input_data = pd.concat([input_state_df, input_data[['YEAR']]], axis=1)

    # predict the total IPC crimes for the input values
    predicted_ipc_crimes = model.predict(input_data)

    # print the predicted total IPC crimes
    
    print('Predicted Total IPC Crimes:', abs(predicted_ipc_crimes))
    
    
    crime_rates.append(abs(predicted_ipc_crimes[0]))
    fig, ax = plt.subplots()
    # plot the line graph of crime rate against year
    ax.bar(year, crime_rates)
    ax.set_xticks([year])  # set the x-axis ticks to show all the years
    ax.set_xlabel('Year')
    ax.set_ylabel('Crime Rate')
    ax.set_title(f'Crime Rate for {state} of the year {year}')
    path = f'static/assets/predict/image{num}.png'
    
    fig.savefig(path)

    return path
    #plt.show()

# predict_range('DODOMA',2016,2019,'UNNATURAL_OFFENCE')
# predict('DODOMA',2019,'UNNATURAL_OFFENCE')