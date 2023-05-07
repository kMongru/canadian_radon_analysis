from sklearn.linear_model import LinearRegression
from sklearn.model_selection import ShuffleSplit
from sklearn import svm
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
    x_train, x_test, y_train, y_test = train_test_split(df, label, test_size = 0.4, random_state = 0)

    radonTest = x_test[dependentVar]

    x_train = x_train.drop([dependentVar], axis=1)
    x_test = x_test.drop([dependentVar], axis=1)

    reg = LinearRegression()
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

    # Cross validation
    print("Cross-validation: ")
    clf = svm.SVC(kernel='linear', C=1, random_state=42)
    cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
    cross_val_score(clf, df, label, cv=cv)

    # How many points are there that are very far apart
    # outliers
    # in test set, we had radon value of more than 7k
    # investigate why we predicted 200 when the point is 7k - what is the difference between these?
    # find max and min values in this dataset - the dataset might be skewed, so we have to remove those outliers
    # 


linreg("tensorflow_continuous.csv", "activity")


