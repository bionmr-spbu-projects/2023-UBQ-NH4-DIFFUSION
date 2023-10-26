import argparse
import pandas as pd
import os

from scipy.optimize import curve_fit

from process_utils.fit import exponential_fit

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='fit tumbling autocorrelation function')
    parser.add_argument('--path-to-tumbling-acorr-csv',
                        help="set path to tumbling_acorr_avg.csv with header [time_ns,acorr]", required=True)
    parser.add_argument('--output-directory', help="set output directory", default=".")

    args = parser.parse_args()

    df_tumbling_acorr = pd.read_csv(args.path_to_tumbling_acorr_csv)

    mask = (df_tumbling_acorr.time_ns >= 0) & (df_tumbling_acorr.time_ns <= 2)

    acorr, time = df_tumbling_acorr["acorr"], df_tumbling_acorr["time_ns"]

    tau_rot, _ = curve_fit(exponential_fit,
                           time[mask],
                           acorr[mask],
                           )
    os.makedirs(args.output_directory, exist_ok=True)
    pd.DataFrame({'exp-1-a1': 1,
                  'exp-1-tau1': tau_rot,
                  'limit_ns': 2,
                  }, index=[0]).to_csv(os.path.join(args.output_directory, "fit.csv"))
