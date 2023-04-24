
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pickle

import xgboost as xgb
from itertools import chain, combinations
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd
import os

file_path = os.path.abspath('../canadian_radon_analysis/Rhys/data/radon-data.csv')
# Data cleaning
df = pd.read_csv(file_path)
df = df.drop(columns=["time", "state_time", "id", "sensor_id", "state"])

df_summer = df.iloc[36000:48000]

summer_min = df_summer.min() # needed to de-normalize data
summer_max = df_summer.max()

df_summer_normalized = (df_summer - summer_min) / (summer_max - summer_min)

df = df_summer_normalized


# Finding Best Trained Model

# Independent variables
independent_vars = ["temperature", "humidity", "pressure", "tvoc"]

# Function to get all combinations of the independent variables
def all_combinations(variables):
    return list(chain(*map(lambda x: combinations(variables, x), range(1, len(variables) + 1))))

# Get all combinations of independent variables
combinations = all_combinations(independent_vars)

# Dependent variable
dependent_var = "radon"

# Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(df[independent_vars], df[dependent_var], test_size=0.2, random_state=42)

# Initialize a dictionary to store mean cross-validation scores
mean_cv_scores = {}

# Number of folds for cross-validation
cv_folds = 5

# Iterate over each combination of independent variables
for combo in combinations:
    # Train an XGBoost regression model
    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42) # Adjust hyperparameters as needed
    
    # Perform cross-validation and calculate mean score
    cv_scores = cross_val_score(model, X_train[list(combo)], y_train, cv=cv_folds, scoring='r2')
    mean_cv_score = np.mean(cv_scores)
    
    # Store the mean cross-validation score in a dictionary
    mean_cv_scores[combo] = mean_cv_score

# Find the combination with the highest mean cross-validation score
best_combo = max(mean_cv_scores, key=mean_cv_scores.get)

"""
print("Best combination of independent variables:", best_combo)
print("Highest mean cross-validation score:", mean_cv_scores[best_combo])
"""

# Train the final model using the best combination of independent variables and the entire training set
best_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42) # Adjust hyperparameters as needed
best_model.fit(X_train[list(best_combo)], y_train)

# Make predictions using the test set
y_pred = best_model.predict(X_test[list(best_combo)])

# Calculate R-squared score
r2 = r2_score(y_test, y_pred)

print("R-squared score on the test set:", r2)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, y_pred)

print("Mean Squared Error on the test set:", mse)

X_train, X_test, y_train, y_test = train_test_split(df[independent_vars], df[dependent_var], test_size=0.2, random_state=42)

summer_min = df_summer.min()
summer_max = df_summer.max()

r2_best_scores = {}
mae_best_scores = {}
mse_best_scores = {}

best_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
best_model.fit(X_train[list(best_combo)], y_train)

y_pred = best_model.predict(X_test[list(best_combo)])

r2_best = r2_score(y_test, y_pred)
mae_best = mean_absolute_error(y_test, y_pred)
mse_best = mean_squared_error(y_test, y_pred)

mse_unnormalized = mse_best * (summer_max["radon"] - summer_min["radon"])**2
mae_unnormalized = mae_best * (summer_max["radon"] - summer_min["radon"])


print("Best combination of independent variables:", best_combo)
print("Highest R-squared score:", r2_best)
print("Mean Squared Error - Unnormalized:", mse_unnormalized)
print("Mean Absolute Error - Unnormalized:", mae_unnormalized)
print("Mean Squared Error:", mse_best)
print("Mean Absolute Error:", mae_best)

## Outputting to pickle
filename = 'finalized_decision_model.sav'
pickle.dump(best_model, open(filename, 'wb'))