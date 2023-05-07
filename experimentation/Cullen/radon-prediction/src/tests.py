from scipy import stats
import pandas as pd
import numpy as np

df = pd.read_csv("../data/radon-data.csv")

radon = df.radon.values.flatten()
state = df.state.values.flatten() == "On"

print(stats.pointbiserialr(state, radon))
