import csv
import os
import numpy as np
import pandas as pd

from tqdm import tqdm

from pyxmolpp2.pipe import TrajectoryProcessor
from pyxmolpp2 import Frame, aName, calc_autocorr_order_2


class CalcTumblingAcorr(TrajectoryProcessor):

    def __init__(self,
                 dt_ns,
                 nodes_coords,
                 nodes_weghts,
                 reference=None,
                 out_filename="tumbling_acorr_avg.csv",
                 out_dirname="."):
        self.dt_ns = dt_ns
        self.nodes_coords = nodes_coords
        self.nodes_weghts = nodes_weghts
        self.reference = reference
        self.out_filename = out_filename
        self.out_dirname = out_dirname
        self.vectors = [[] for _ in self.nodes_coords]

    def before_first_iteration(self, frame: Frame) -> None:
        # set selection of CA atoms for alignment
        self._reference = self.reference or Frame(frame)
        self.ref_ca_atoms = self.reference.atoms.filter(aName == "CA")
        self.frame_ca_atoms = frame.atoms.filter(aName == "CA")

    def after_last_iteration(self, exc_type, exc_value, traceback) -> bool:
        avg_acorr = 0
        for weight, vector in tqdm(zip(self.nodes_weghts, self.vectors)):
            avg_acorr += calc_autocorr_order_2(vector) * weight
        avg_acorr = avg_acorr / 4 / np.pi

        os.makedirs(self.out_dirname, exist_ok=True)
        T = np.linspace(0, len(avg_acorr) * self.dt_ns, len(avg_acorr))
        df = pd.DataFrame(np.array([T, avg_acorr]).T, columns=["time_ns", "acorr"])
        df.to_csv(os.path.join(self.out_dirname, self.out_filename), index=False)

        return False

    def __call__(self, frame: Frame) -> Frame:
        # get trajectories of
        alignment = self.frame_ca_atoms.alignment_to(self.ref_ca_atoms)
        matrix3d = alignment.matrix3d()

        for ind, node in enumerate(self.nodes_coords):
            self.vectors[ind].append(matrix3d.dot(node))

        return frame
