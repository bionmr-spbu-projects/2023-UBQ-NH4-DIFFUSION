import argparse
import pandas as pd
import os
from scipy.optimize import curve_fit

from process_utils.fit import linear_fit

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Linear fit of the mean square displacement (MSD) curve')
    parser.add_argument('--path-to-msd-csv', help="set path to msd.csv with header [time_ns,msd]", required=True)
    parser.add_argument('--output-directory',  help="set output directory", default=".")
    args = parser.parse_args()

    df = pd.read_csv(args.path_to_msd_csv)
    mask = (df.time_ns >= 0.1) & (df.time_ns <= 1)

    p_coeff, _ = curve_fit(linear_fit,
                           df["time_ns"][mask],
                           df["msd"][mask]
                           )

    pd.DataFrame({
        "k": [p_coeff[0]],
        "b": [p_coeff[1]]}
    ).to_csv(os.path.join(args.output_directory, "fit.csv"), index=False)
