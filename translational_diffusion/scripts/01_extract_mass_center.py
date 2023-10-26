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
    parser.add_argument('--path-to-trajectory', help="set path to directory with trajectory files", required=True)
    parser.add_argument('--path-to-reference-pdb', help="set path to reference pdb", required=True)
    parser.add_argument('--dt-ns', help="time step between frame in trajectory", required=True, type=float)
    parser.add_argument('--filetype', help="specify engine which you used: nc for Amber, xtc for Gromacs",
                        choices=["dat", "nc", "xtc"], required=True)
    parser.add_argument('--pattern',
                        help="assumed that trajectory saved as N files: run00001.nc, run00002.nc, ... run0000N.nc",
                        default="run%05d")
    parser.add_argument('--trajectory-start', help="first nanosecond to be read", default=1, type=int)
    parser.add_argument('--trajectory-length', help="last nanosecond to be read", required=True, type=int)
    parser.add_argument('--frames-per-trajectory-file', help="number of frames in 1 trajectory file", type=int,
                        default=100)
    parser.add_argument('--output-directory', help="set output directory", default=".")
    args = parser.parse_args()

    trj_reader_dict = {"dat": TrjtoolDatFile,
                       "nc": AmberNetCDF,
                       "xtc": XtcFileReaderWrapper(args.frames_per_trajectory_file)}

    #  load reference
    reference = PdbFile(args.path_to_reference_pdb).frames()[0]
    reference.atoms.guess_mass()

    #  load trajectory
    traj = Trajectory(PdbFile(args.path_to_reference_pdb).frames()[0])
    for ind in tqdm(range(args.trajectory_start, args.trajectory_length + 1), desc="traj_reading"):
        fname = "{pattern}.{filetype}".format(pattern=args.pattern, filetype=args.filetype)
        traj.extend(trj_reader_dict[args.filetype](os.path.join(args.path_to_trajectory, fname % (ind))))

    #  process trajectory in pipe-like format
    tqdm(traj | ExtractMassCenter(dt_ns=args.dt_ns, out_dirname=args.output_directory)) | Run()
