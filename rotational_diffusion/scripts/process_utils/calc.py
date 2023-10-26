import os
import numpy as np
import pandas as pd

from tqdm import tqdm
from typing import List

from pyxmolpp2.pipe import TrajectoryProcessor
from pyxmolpp2 import Frame, aName, calc_autocorr_order_2


class CalcTumblingAcorr(TrajectoryProcessor):

    def __init__(self,
                 dt_ns: float,
                 nodes_coords: List[List],
                 nodes_wegihts: List[List],
                 reference: Frame = None,
                 out_filename: str = "tumbling_acorr_avg.csv",
                 out_dirname: str = ".") -> None:
        """
        The idea is to run of the processing trajectory in pipe-like format:
        trajectory | CalcTumblingAcorr(dt_ns=0.001) | Run()
        Towards to this aim, pseudo-trajectories that encodes the protein’s tumbling motion are generated for
        vectors near-uniform distributed on a unit sphere. The final autocorrelation function is average for
        individual autocorrelation function calculated over each  pseudo-trajectory.


        :param dt_ns: time step between frame in trajectory
        :param nodes_coords: coordinates of vectors near-uniform distributed on a unit sphere [N, 3]
        :param nodes_wegihts: weights of vectors near-uniform distributed on a unit sphere [N, 1]
        :param reference: trajectory reference, by default used the first frame of trajectory
        :param out_filename: by default tumbling_acorr_avg.csv
        :param out_dirname: by default the current directory
        """
        self.dt_ns = dt_ns
        self.nodes_coords = nodes_coords
        self.nodes_wegihts = nodes_wegihts
        self.reference = reference
        self.out_filename = out_filename
        self.out_dirname = out_dirname
        self.vectors = [[] for _ in self.nodes_coords]

    def before_first_iteration(self, frame: Frame) -> None:
        """
        this function will be called before the first iteration over trajectory
        :param frame:
        :return:
        """
        # set selection of CA atoms for alignment
        self._reference = self.reference or Frame(frame)
        self.ref_ca_atoms = self._reference.atoms.filter(aName == "CA")
        self.frame_ca_atoms = frame.atoms.filter(aName == "CA")

    def after_last_iteration(self, exc_type, exc_value, traceback) -> bool:
        """
        this function will be called after the last iteration over trajectory
        :param exc_type:
        :param exc_value:
        :param traceback:
        :return:
        """
        avg_acorr = 0
        for weight, vector in tqdm(zip(self.nodes_wegihts, self.vectors)):
            avg_acorr += calc_autocorr_order_2(vector) * weight
        avg_acorr = avg_acorr / 4 / np.pi

        os.makedirs(self.out_dirname, exist_ok=True)
        T = np.linspace(0, len(avg_acorr) * self.dt_ns, len(avg_acorr))
        df = pd.DataFrame(np.array([T, avg_acorr]).T, columns=["time_ns", "acorr"])
        df.to_csv(os.path.join(self.out_dirname, self.out_filename), index=False)

        return False

    def __call__(self, frame: Frame) -> Frame:
        """
        this function will be called for each iteration over trajectory
        :param frame:
        :return:
        """
        # get trajectories of
        alignment = self.frame_ca_atoms.alignment_to(self.ref_ca_atoms)
        matrix3d = alignment.matrix3d()

        for ind, node in enumerate(self.nodes_coords):
            self.vectors[ind].append(matrix3d.dot(node))

        return frame
