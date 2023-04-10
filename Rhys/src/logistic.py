import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from itertools import chain, combinations
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

# Data cleaning
df_logistic_reg = pd.read_csv('../data/radon-data.csv')
df_logistic_reg = df_logistic_reg.drop(columns=["time", "state_time", "id", "sensor_id"])
df_logistic_reg['state'] = df_logistic_reg['state'].replace({'Off': 0, 'On': 1})

df_logistic_reg['radon_binary'] = df_logistic_reg['radon'].apply(lambda x: 1 if x > 300 else 0)
df_logistic_reg = df_logistic_reg.drop(columns=["radon"])

df_logistic_reg['temperature'] = df_logistic_reg['temperature'].astype(float)

# Independent variables
independent_vars = ["temperature", "humidity", "pressure", "tvoc", "state"]

# Function to get all combinations of the independent variables
def all_combinations(variables):
    return list(chain(*map(lambda x: combinations(variables, x), range(1, len(variables) + 1))))

# Get all combinations of independent variables
combinations = all_combinations(independent_vars)

# Dependent variable
dependent_var = "radon_binary"

# Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(df_logistic_reg[independent_vars], df_logistic_reg[dependent_var], test_size=0.2, random_state=42)

# Initialize a dictionary to store accuracy scores
accuracy_scores = {}

# Iterate over each combination of independent variables
for combo in combinations:
    # Train a logistic regression model
    model = LogisticRegression(max_iter=1000) # Increase max_iter if the algorithm does not converge
    model.fit(X_train[list(combo)], y_train)

    # Make predictions using the test set
    y_pred = model.predict(X_test[list(combo)])

    # Calculate accuracy score
    accuracy = accuracy_score(y_test, y_pred)

    # Store the accuracy score in the dictionary
    accuracy_scores[combo] = accuracy

# Find the combination with the highest accuracy score
best_combo = max(accuracy_scores, key=accuracy_scores.get)

print("Best combination of independent variables:", best_combo)
print("Highest accuracy score:", accuracy_scores[best_combo])

scaler = StandardScaler()
train_scaled = scaler.fit_transform(independent_vars) # Fit the scaler to the training data
pickle.dump(scaler, open('scaler.pkl','wb')) # Save the scaler for later use (Example: To transform new data to predict)
model = LogisticRegression()
model.fit(train_scaled, dependent_var)
filename = 'model.sav'
pickle.dump(model, open(filename, 'wb')) # Save the model for later use