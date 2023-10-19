## 1. change the path to SCRIPT_DIR according to your directory tree
SCRIPT_DIR:={YOUR PATH}/2023-UBQ-NH4-DIFFUSION/translational_diffusion/scripts/

## secify file with vectors (emulating N-HN bonds) with near-uniform distribution on a unit sphere
## Here, we used 64 vectors downloaded from http://www.personal.soton.ac.uk/jf1w07/nodes/nodes.html
NODES_PATH:="${SCRIPT_DIR}/../data/64_nodes.csv"

## 3. specify MD trajectory parameters
# set path to trajectory
TRAJECTORY_PATH:=""
# set path to reference pdb
REFERENCE_PDB_PATH:=""
# set trajectory length to be processed
TRAJECTORY_LENGTH:="" # ns
# set type of trajectory files: "dat" - TrjtoolDatFile; "nc" - AmberNetCDF; "xtc" - GromacsXtcFile
FILETYPE:=nc
# set pattern for trajectory filenames: run00001.dat ---> "run%05d".dat
PATTERN:=run%05d
# set timestep used to record trajectory files
DT_NS=0.001 # ns