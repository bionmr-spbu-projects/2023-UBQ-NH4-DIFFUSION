<div align="justify">

# Calculation of diffusion coefficients (Dtr, Drot) from MD trajectories

This repository contains the scripts and sample data for calculation of translational and rotational diffusion
coefficients from MD trajectory

### System requirements

Key packages and programs:

- Linux platform (tested on ubuntu 20.04 and ubuntu 22.04)
- [python3](https://www.python.org/)
- [gcc compiler](https://gcc.gnu.org/) (7.0 <= version <= 11.0)
- [g++ compiler](https://gcc.gnu.org/) (7.0 <= version <= 11.0)
- [cmake](https://www.gnu.org/software/make/manual/make.html)

### Installation dependencies

The key package to analyze an MD trajectory is the python
library [pyxmolpp2](https://sizmailov.github.io/pyxmolpp2/api/python/install.html) 
written in-house

```code-block:: bash
# install system dependencies
sudo apt-get install g++ gcc cmake python3 python3-dev libnetcdf-dev 

# create virtual enviroment
python3 -m venv ./venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -U setuptools wheel pip

# install python packages
pip install -r requirements.txt
```

### Run MD analyses

Please, see github pages for the relevant type of calculations:

1) [Translational diffusion coefficient Dtr](translational_diffusion/README.md)
2) [Rotational diffusion coefficient Drot](rotational_diffusion/README.md)

</div>



