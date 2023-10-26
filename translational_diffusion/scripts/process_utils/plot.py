import matplotlib.pyplot as plt
import pandas as pd
import os

from .fit import linear_fit


def plot_msd_with_fit(path_to_msd_csv: str,
                      path_to_fit_msd_csv: str,
                      output_directory: str
                      ) -> None:
    """
    This script saves the figure of MSD curve and its linear fit

    :param path_to_msd_csv:
    :param path_to_fit_msd_csv:
    :param output_directory:
    :return:
    """
    df_msd = pd.read_csv(path_to_msd_csv)
    df_msd = df_msd[df_msd.time_ns < 3]
    fit = pd.read_csv(path_to_fit_msd_csv)

    fig = plt.figure()  # type:plt.Figure
    ax = fig.add_subplot(111)  # type: plt.Axes
    ax.plot(df_msd.time_ns, df_msd.msd, label="")

    p_coeff = fit[["k", "b"]].values[0]
    ax.plot(df_msd.time_ns, linear_fit(df_msd.time_ns, *p_coeff),
            label="D = {:.3e} $m^2/s$".format(fit["b"][0] * 1e-10 ** 2 / 1e-9 / 6))

    ax.set_xlabel('time, ns', fontsize=13)
    ax.set_ylabel(r'MSD, $\AA^2$', fontsize=13)
    ax.axvline(1, color='g', linestyle='--')
    ax.grid(True)
    ax.legend()
    plt.savefig(os.path.join(output_directory, "fit_msd_plot.png"))
    plt.close()
