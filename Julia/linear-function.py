from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

# Function to find linear regression

def linreg(csvData, dependentVar):
    path = './data/' + csvData
    df = pd.read_csv(path, encoding='latin-1')
    
    label = df[dependentVar]
    train = df.drop([dependentVar], axis=1)

    x_train, x_test, y_train, y_test = train_test_split(train, label, test_size = 0.1, random_state = 2)

    reg = LinearRegression()
    print(reg.fit(x_train, y_train)) # Fit the linear model
    preds = reg.predict(x_test)
    print("R squared value: ", r2_score(y_test, preds))
    print("Coefficient of determination of the prediction: ", reg.score(x_test, y_test)) # Return the coefficient of determination of the prediction

linreg("tensorflow_continuous.csv", "activity")

