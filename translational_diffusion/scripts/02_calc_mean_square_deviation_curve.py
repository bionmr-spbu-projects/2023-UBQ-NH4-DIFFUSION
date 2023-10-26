import argparse
import os
import pandas as pd

from process_utils.calc import calc_mean_square_displacement

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate mean square displacement (MSD) of center of mass (msd)')

    parser.add_argument('--path-to-cm-csv', help="set path to cm.csv with header [time_ns,cm_x,cm_y,cm_z]")
    parser.add_argument('--msd-length-ns',
                        help="set length of msd curve, by default 10 ns. It's enough, because only 1 ns used for fit",
                        default=10, type=int)
    parser.add_argument('--output-directory', help="set output directory", default=".")
    args = parser.parse_args()

    df_cm = pd.read_csv(args.path_to_cm_csv)
    mask = df_cm.time_ns <= args.msd_length_ns
    df_cm = df_cm[mask]

    time = df_cm["time_ns"]
    xyz = df_cm[["cm_x", "cm_y", "cm_z"]].values

    lag_index = list(range(1, time.size))
    lag, msd = calc_mean_square_displacement(time, xyz, lag_index=lag_index)

    pd.DataFrame({
        "time_ns": lag,
        "msd": msd,
    }).to_csv(os.path.join(args.output_directory, "msd.csv"), index=False)
