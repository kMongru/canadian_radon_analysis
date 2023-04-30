
def predict_radon(temp, humidity, pressure, tvoc):
    import pandas as pd
    import pickle
    import xgboost as xgb
    
    # Load the pickled model object
    with open('./Rhys/src/serialized_objects.pickle', 'rb') as f:
        model_object = pickle.load(f)

    # Access the df_summer dataframe from the model object
    df_summer = model_object['df_summer']

    summer_min = df_summer.min()
    summer_max = df_summer.max()

    independent_min = df_summer.drop(columns=["radon"]).min()
    independent_max = df_summer.drop(columns=["radon"]).max()

    new_data = {"temperature": temp, "humidity": humidity, "pressure": pressure, "tvoc": tvoc}

    new_data_df = pd.DataFrame(new_data, index=[0])

    new_data_normalized = (new_data_df - independent_min) / (independent_max - independent_min)

    prediction = model_object['best_model'].predict(new_data_normalized.values.reshape(1, -1))[0]
    ##prediction = best_model.predict(pd.DataFrame([new_data_normalized])[list(best_combo)])

    unnormalized_prediction = prediction * (summer_max["radon"] - summer_min["radon"]) + summer_min["radon"]

    print("Predicted radon concentration", unnormalized_prediction)
    return unnormalized_prediction

predict_radon(25, 50, 1017, 2)