import numpy as np


def exponential_fit(time, tau):
    return np.exp(-time / tau)
