"""Machine Learning Tutorial #1: Linear Regression. """

import quandl as qd
import pandas as pd
import numpy as np
import math
import pickle
from sklearn import preprocessing, svm, model_selection
from sklearn.linear_model import LinearRegression as LR


# Dataframe of google stock prices
df = quandl.get("WIKI/GOOGL")

# Subsetting to the variables we need
df = df[["Adj. Open", "Adj. High", "Adj. Low", "Adj. Close"]]
df["HL_PCT"] = (df["Adj. Open"] - df["Adj. Close"]) / df["Adj. Close"] * 100.0
df["PCT_change"] = (df["Adj. Close"] - df["Adj. Open"]) / df["Adj. Open"] * 100.0

# dataframe of our features and label
df = df[["Adj. Close", "HL_PCT", "PCT_change"]]
forecast_col = "Adj. Close"

# In machine learning, you can't work with nan's so:
df.fillna(-99999, inplace=True)

# Create future prices
forecast_out = int(math.ceil(0.01 * len(df)))

# Define our label = Y
df["label"] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)

# Feature = X, Label = Y. Transform to numpy array for speed
X = np.array(df.drop(["label"], 1))  # Drops every column except "label"
Y = np.array(df["label"])

# Skip this step if too many features
X = preprocessing.scale(X)

X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.2)

# Our classifier = regression or svm=support vector machines

# Regression
clf = LR()
clf.fit(X_train, Y_train)

# Pickle this to avoid redoing/retrain an algorithm
with open("Linear_regression.pickle", "wb") as f:
    pickle.dump(clf, f)

pickle_in = open("Linear_regression.pickle", "rb")
clf = pickle.load(pickle_in)

accuracy = clf.score(X_test, Y_test)
print(accuracy)

# SVM
clf = svm.SVR(kernel="poly")
clf.fit(X_train, Y_train)
accuracy = clf.score(X_test, Y_test)
print(accuracy)

