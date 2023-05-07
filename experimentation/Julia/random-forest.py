# This file runs random forest based on the dataset input.

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
from sklearn.metrics import r2_score

def column(matrix, i):
    return [row[i] for row in matrix]

# Function to find linear regression

def linreg(csvData, dependentVar):
    path = './data/' + csvData
    df = pd.read_csv(path, encoding='latin-1')
    
    label = df[dependentVar]
    x_train, x_test, y_train, y_test = train_test_split(df, label, test_size = 0.2, random_state = 2)

    radonTest = x_test[dependentVar]

    x_train = x_train.drop([dependentVar], axis=1)
    x_test = x_test.drop([dependentVar], axis=1)

    reg = RandomForestRegressor()
    reg.fit(x_train, y_train) # Fit the linear model
    preds = reg.predict(x_test)
    print("R squared value: ", r2_score(y_test, preds))
    print("Coefficient of determination of the prediction: ", reg.score(x_test, y_test)) # Return the coefficient of determination of the prediction
    #print("Coefficients: ", reg.coef_)
    print("Mean squared error: ", mean_squared_error(y_test, preds))
    print("Mean absolute error: ", mean_absolute_error(y_test, preds))

    
    # Plotting
    plt.scatter(radonTest, preds)
    plt.show()



linreg("tensorflow_continuous.csv", "activity")


