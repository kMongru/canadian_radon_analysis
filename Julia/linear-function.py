from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
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
    train = df.drop([dependentVar], axis=1)

    x_train, x_test, y_train, y_test = train_test_split(train, label, test_size = 0.2, random_state = 2)

    reg = LinearRegression()
    print(reg.fit(x_train, y_train)) # Fit the linear model
    preds = reg.predict(x_test)
    print("R squared value: ", r2_score(y_test, preds))
    print("Coefficient of determination of the prediction: ", reg.score(x_test, y_test)) # Return the coefficient of determination of the prediction
    print("Coefficients: ", reg.coef_)
    print("Mean squared error: ", mean_squared_error(y_test, preds))

    # Find dependent variable column index
    colIndex = df.columns.get_loc(dependentVar)
    res = np.array(x_test)[:,colIndex] # prepping test matrix for plotting

    # Plotting
    plt.scatter(res, preds)
    plt.show()




linreg("tensorflow_continuous.csv", "activity")


