import argparse
import os
from tqdm import tqdm
from pyxmolpp2 import PdbFile, Trajectory, TrjtoolDatFile, AmberNetCDF, GromacsXtcFile
from pyxmolpp2.pipe import Run

from process_utils.extract import ExtractMassCenter


class XtcFileReaderWrapper:
    def __init__(self, n_frames):
        self.n_frames = n_frames

    def __call__(self, filename):
        return GromacsXtcFile(filename, self.n_frames)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract mass center')
    parser.add_argument('--path-to-trajectory', required=True)
    parser.add_argument('--path-to-reference-pdb', required=True)
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

    tqdm(traj | ExtractMassCenter(dt_ns=args.dt_ns, out_dirname=args.output_directory)) | Run()
