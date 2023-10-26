## 1. change the path to SCRIPT_DIR according to your directory tree
SCRIPT_DIR:=../../../2023-UBQ-NH4-DIFFUSION/rotational_diffusion/scripts/

## specify file with vectors (emulating N-HN bonds) with near-uniform distribution on a unit sphere
## Here, we used 64 vectors downloaded from http://www.personal.soton.ac.uk/jf1w07/nodes/nodes.html
NODES_PATH:="${SCRIPT_DIR}/../data/64_nodes.csv"

## 3. specify MD trajectory parameters
# set path to trajectory
TRAJECTORY_PATH:="../../short_example_trajectory/UBQ"
# set path to reference pdb
REFERENCE_PDB_PATH:="../../short_example_trajectory/UBQ/reference.pdb"
# set trajectory length to be processed
TRAJECTORY_LENGTH:=10 # ns
# set type of trajectory files: "dat" - TrjtoolDatFile; "nc" - AmberNetCDF; "xtc" - GromacsXtcFile
FILETYPE:=nc
# set pattern for trajectory filenames: run00001.dat ---> "run%05d".dat
PATTERN:=run%05d
# set timestep used to record trajectory files
DT_NS=0.001 # ns