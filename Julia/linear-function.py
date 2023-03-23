{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.linear_model import LinearRegression\n",
    "from sklearn.model_selection import train_test_split\n",
    "\n",
    "# Function to find linear regression\n",
    "csvData = input(\"Enter the csv database you want to perform a linear regression on: \")\n",
    "dependentVar = input(\"Enter the column name of the dependent variable: \") \n",
    "\n",
    "def linreg(csvData, dependentVar):\n",
    "    path = '../discovery/data/' + csvData\n",
    "    df = pd.read_csv(path, encoding='latin-1')\n",
    "\n",
    "    label = df[dependentVar]\n",
    "    train = df.drop([label], axis=1)\n",
    "\n",
    "    x_train, x_test, y_train, y_test = train_test_split(train1, labels, test_size = 0.10, random_state = 2)\n",
    "\n",
    "    reg = LinearRegression()\n",
    "\n",
    "    print(reg.fit(x_train, y_train)) # Fit the linear model\n",
    "    print(\"Coefficient of determination of the prediction: \", reg.score(x_test, y_test)) # Return the coefficient of determination of the prediction\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
