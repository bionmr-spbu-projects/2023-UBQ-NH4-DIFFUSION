import argparse
import os
import pandas as pd
from tqdm import tqdm
from pyxmolpp2 import PdbFile, Trajectory, TrjtoolDatFile, AmberNetCDF, GromacsXtcFile
from pyxmolpp2.pipe import Run

from process_utils.calc import CalcTumblingAcorr


class XtcFileReaderWrapper:
    def __init__(self, n_frames):
        self.n_frames = n_frames

    def __call__(self, filename):
        return GromacsXtcFile(filename, self.n_frames)


#
# def extract_inertia_tensor_vectors_autocorr(output_directory: str,
#                                             ):
#     os.makedirs(output_directory, exist_ok=True)
#
#     ref = traj[0]
#     ref_ca = ref.asAtoms.filter(aName == "CA")
#     frame_ca = None
#
#     nodes = pd.read_csv("/home/sergei/GB1/nodes/64.txt.csv", names=["x", "y", "z", "w"])
#     xyz = nodes[["x", "y", "z"]].values
#     weights = nodes["w"]
#
#     vectors = [VectorXYZ() for v in xyz]
#
#     for frame in tqdm(traj, desc="extract vectors"):
#         if frame_ca is None:
#             frame_ca = frame.asAtoms.filter(aName == "CA")
#
#         al = ref_ca.alignment_to(frame_ca)
#         m = al.matrix3d()
#         for vector, node in zip(vectors, xyz):
#             v1 = m.dot(node)
#             vector.append(XYZ(v1[0], v1[1], v1[2]))
#
#     sum_acorr = None
#     for i, vector in enumerate(tqdm(vectors, desc="calc autocorr")):
#         w = weights[i]
#         autocorr = np.array(calc_autocorr_order_2(vector, 1000 * 100)) * w
#         if sum_acorr is None:
#             sum_acorr = autocorr
#         else:
#             sum_acorr += autocorr
#     avg_acorr = sum_acorr / 4 / np.pi
#     T = np.linspace(0, len(avg_acorr) * extract_time_step_ns(path_to_trajectory), len(avg_acorr))
#     df = pd.DataFrame(np.array([T, avg_acorr]).T, columns=["time_ns", "acorr"])
#     df.to_csv(os.path.join(output_directory, "tumbling_avg.csv"), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract mass center')
    parser.add_argument('--path-to-trajectory', required=True)
    parser.add_argument('--path-to-reference-pdb', required=True)
    parser.add_argument('--path-to-nodes-csv', required=True)
    parser.add_argument('--dt-ns', required=True, type=float)
    parser.add_argument('--filetype', choices=["dat", "nc", "xtc"], required=True)
    parser.add_argument('--pattern', default="run%05d")
    parser.add_argument('--trajectory-start', default=1, type=int)
    parser.add_argument('--trajectory-length', required=True, type=int)
    parser.add_argument('--frames-per-trajectory-file', type=int, default=100)
    parser.add_argument('--output-directory', default=".")
    args = parser.parse_args()

    trj_reader_dict = {"dat": TrjtoolDatFile,
                       "nc": AmberNetCDF,
                       "xtc": XtcFileReaderWrapper(args.frames_per_trajectory_file)}

    #  load trajectory
    reference = PdbFile(args.path_to_reference_pdb).frames()[0]
    reference.atoms.guess_mass()

    traj = Trajectory(PdbFile(args.path_to_reference_pdb).frames()[0])
    for ind in tqdm(range(args.trajectory_start, args.trajectory_length + 1), desc="traj_reading"):
        fname = "{pattern}.{filetype}".format(pattern=args.pattern, filetype=args.filetype)
        traj.extend(trj_reader_dict[args.filetype](os.path.join(args.path_to_trajectory, fname % (ind))))

    # read nodes
    nodes = pd.read_csv(args.path_to_nodes_csv, names=["x", "y", "z", "w"])
    nodes_coords = nodes[["x", "y", "z"]].values
    nodes_weghts = nodes["w"]

    tqdm(traj | CalcTumblingAcorr(dt_ns=args.dt_ns,
                                  reference=traj[0],
                                  nodes_coords=nodes_coords,
                                  nodes_weghts=nodes_weghts,
                                  out_dirname=args.output_directory
                                  )) | Run()
