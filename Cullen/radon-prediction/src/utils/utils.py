import numpy as np
import pandas as pd


def generate_windows(data, x_len, y_len):
    """
    Builds the windowed version of data, given the length of x_len and y_len.

    Params:
    =======
    @param data: list or array
    @param x_len: int. Length of the training set
    @param y_len: int. Length of the forecast
    """
    N = x_len + y_len
    return np.array([
        pd.Series(data).shift(i) for i in reversed(range(N))
    ]).transpose()[N - 1:, :]


def mix_data(data):
    """Custom function to format properly the data"""
    complete = np.empty((list(data["radon"].shape) + [len(data.keys())]))
    keys = list(data.keys())
    for i in range(len(keys)):
        complete[:, :, i] = data[keys[i]]
    return complete
