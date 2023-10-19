import argparse
from process_utils.plot import plot_msd_with_fit
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot mean square displacement (MSD) curve with fit')
    parser.add_argument('--path-to-msd-csv', required=True)
    parser.add_argument('--path-to-fit-csv', required=True)
    parser.add_argument('--output-directory', default=os.getcwd())
    args = parser.parse_args()
    plot_msd_with_fit(args.path_to_msd_csv, args.path_to_fit_csv, args.output_directory)
