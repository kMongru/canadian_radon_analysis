import json
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
from sklearn.linear_model import LinearRegression


def handle_prediction(humidity, pressure, temperature, tvoc):    
    # Load the pickled model object
    with open('serialized_objects.pickle', 'rb') as f:
        model_object = pickle.load(f)

    # Access the df_summer dataframe from the model object
    df_summer = model_object['df_summer']

    summer_min = df_summer.min()
    summer_max = df_summer.max()

    independent_min = df_summer.drop(columns=["radon"]).min()
    independent_max = df_summer.drop(columns=["radon"]).max()

    new_data = {"temperature": temperature, "humidity": humidity, "pressure": pressure, "tvoc": tvoc}

    new_data_df = pd.DataFrame(new_data, index=[0])

    new_data_normalized = (new_data_df - independent_min) / (independent_max - independent_min)

    prediction = model_object['best_model'].predict(new_data_normalized.values.reshape(1, -1))[0]
    ##prediction = best_model.predict(pd.DataFrame([new_data_normalized])[list(best_combo)])

    unnormalized_prediction = prediction * (summer_max["radon"] - summer_min["radon"]) + summer_min["radon"]

    print("Predicted radon concentration", unnormalized_prediction)
    
    return unnormalized_prediction

def lambda_handler(event, context):
    
    # setting up to handle 
    humidity = event['humidity']
    pressure = event['pressure']
    temperature = event['temperature']
    tvoc = event['tvoc']
    timestamp = event['timestamp']

    radon = handle_prediction(int(humidity), int(pressure), int(temperature), int(tvoc))

    # TODO implement
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type" : 'application/json',
            "Access-Control-Allow-Headers" : 'Content-Type,X-Amz- Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            "Access-Control-Allow-Methods" : 'OPTIONS,GET', 
            "Access-Control-Allow-Credentials" : True, 
            "Access-Control-Allow-Origin" : '*', 
            "X-Requested-With" : '*'
        },
        'body': {
            "radon": radon,
            "timestamp": timestamp
        }
    }
