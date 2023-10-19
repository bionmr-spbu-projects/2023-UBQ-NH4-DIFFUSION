from typing import Tuple
from tqdm import tqdm
import numpy as np


def calc_mean_square_displacement(time: np.array,
                                  mass_centers: np.array,
                                  lag_index: np.array
                                  ) -> Tuple[np.array, np.array]:
    """
    :param time: time-points between mass_centers
    :param mass_centers: N*3 array [x,y,z] columns
    :param lag_index: int array of time lags between mass_centers
    :return: tuple of two arrays (time_lag, msd)
    """

    assert time.shape[0] == mass_centers.shape[0]
    assert mass_centers.shape[1] == 3

    time_lags = []
    msds = []
    for int_lag in tqdm(lag_index):
        lag_time = time[int_lag]
        msd = ((mass_centers[int_lag:] - mass_centers[:-int_lag]) ** 2).sum(axis=1).mean()
        time_lags.append(lag_time)
        msds.append(msd)

    return np.array(time_lags), np.array(msds)
