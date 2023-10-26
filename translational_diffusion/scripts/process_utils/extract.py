from pyxmolpp2.pipe import TrajectoryProcessor
from pyxmolpp2 import Frame
import os
import csv


class ExtractMassCenter(TrajectoryProcessor):

    def __init__(self,
                 dt_ns: float,
                 out_filename: str = "cm.csv",
                 out_dirname: str = ".") -> None:
        """
        The idea is to run of the processing trajectory in pipe-like format:
        trajectory | ExtractMassCenter(dt_ns=0.001) | Run()

        :param dt_ns: time step between frame in trajectory
        :param out_filename: by default cm.csv
        :param out_dirname: by default the current directory
        """

        self.dt_ns = dt_ns
        self.out_filename = out_filename
        self.out_dirname = out_dirname
        self.output_file = None
        self.prev_cm = None

    def before_first_iteration(self, frame: Frame) -> None:
        """
        this function will be called before the first iteration over trajectory
        :param frame:
        :return:
        """
        # open file to write coordinates of mass center
        os.makedirs(self.out_dirname, exist_ok=True)
        self.out_file = open(os.path.join(self.out_dirname, self.out_filename), "w")
        self.out_csvfile = csv.writer(self.out_file)
        self.out_csvfile.writerow(["time_ns", "cm_x", "cm_y", "cm_z"])

    def after_last_iteration(self, exc_type, exc_value, traceback) -> bool:
        """
        this function will be called after the last iteration over trajectory
        :param exc_type:
        :param exc_value:
        :param traceback:
        :return:
        """
        # close file
        self.out_file.close()
        return False

    def __call__(self, frame: Frame) -> Frame:
        """
        this function will be called for each iteration over trajectory
        :param frame:
        :return:
        """
        # extract coordinates of mass center
        frame.atoms.guess_mass()
        current_cm = frame.atoms.mean(weighted=True)

        if self.prev_cm:
            closest = frame.cell.closest_image_to(self.prev_cm, current_cm)
            current_cm += closest.shift

        self.prev_cm = current_cm
        self.out_csvfile.writerow([frame.index * self.dt_ns, *current_cm.values])

        return frame
