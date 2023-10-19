import numpy as np
import os
import pandas as pd
from scipy.optimize import curve_fit


def exponential_fit(time, tau):
    return np.exp(-time / tau)
