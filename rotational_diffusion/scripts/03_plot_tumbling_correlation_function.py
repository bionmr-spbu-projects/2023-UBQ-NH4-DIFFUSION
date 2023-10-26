import argparse
from process_utils.plot import plot_acorr_fit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="plot tumbling autocorrelation function with fit")
    parser.add_argument("--path-to-tumbling-acorr-csv", help="set path to fit.csv (y=kx+b) with header [k,b]",
                        required=True)
    parser.add_argument("--path-to-fit",
                        help="set path to fit.csv (y=exp(-tau_rot/tau)) with header [exp-1-a1,exp-1-tau1,limit_ns]",
                        required=True)
    parser.add_argument("--output-directory", help="set output directory", default=".")
    args = parser.parse_args()
    plot_acorr_fit(args.path_to_fit, args.path_to_acorrs, args.output_directory)
