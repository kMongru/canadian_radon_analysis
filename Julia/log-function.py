import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

def logreg(csvData, dependentVar):
    # Getting the csv file
    path = './data/' + csvData
    df = pd.read_csv(path, encoding='latin-1')

    # Preparing dummy data
    colVals = df.columns
    dummies = colVals.drop(dependentVar)
    dummy_data = pd.get_dummies(df[dummies])
    data = pd.concat([df, dummy_data], axis = 1)
    data.drop(dummies, axis=1, inplace=True)

    # Setting up testing and training
    X = data.drop(dependentVar, axis = 1)
    y = data[dependentVar]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 0)

    # Developing logistic regression
    log_reg = LogisticRegression()
    log_reg.fit(X_train, y_train)
    y_pred = log_reg.predict(X_test)

    print("Y prediction: ", y_pred)
    print("Accuracy score: ", accuracy_score(y_pred, y_test))
    print("Confusion matrix: ", confusion_matrix(y_pred, y_test))

logreg("tensorflow_continuous.csv", "activity")

