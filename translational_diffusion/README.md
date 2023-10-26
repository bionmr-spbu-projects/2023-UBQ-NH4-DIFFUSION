<div align="justify">

# Calculation of translational diffusion coefficient Dtr from MD trajectory

### Theoretical notes

The processing of the MD trajectory includes the following steps:

1) extract positions of the protein’s center of mass R(t)

<p align="center">
  <img src="figures/cm.png">
</p>

where mi and ri refer to atomic masses and atomic coordinates. 

2) calculate mean square displacement MSD(τ) of the protein’s center of mass

<p align="center">
  <img src="figures/msd.png">
</p>

where tj and tj + τ are a pair of time points
separated by the interval τ, and n is a number of such pairs within the trajectory.

3) The obtained dependencies MSD(τ) have been fitted using a linear fitting function to extract Dtr. It is important to
   choose the appropriate τ interval over which the fitting is performed. This interval should not extend to large τ
   values where the accuracy of the MSD(τ) curve suffers from increasingly poor statistics that manifests itself in large correlated errors.
   On the other hand, one can argue that small τ values should also be left out to avoid the effect of fast internal dynamics in the protein molecule.
   In our study of UBQ and 25-residue disordered peptide N-H4, we have chosen the fitting interval [100 ps, 1 ns] to fit MSD(τ) profiles.

### Run scripts

The scripts for calculation of translational diffusion coefficient Dtr were assembeled into a pipeline using make
utility. To process your own trajectory, you need to:

1) copy the template [analysis_template](analysis_template)
2) specify the parameters in [analysis_template/common.mk](analysis_template/common.mk)
3) type make.

### Run tests

We provide the templates to analyze short 10-ns trajectory of ubiquitin (UBQ) recorded using the programm Amber. 
The purpose is to make sure that all scripts run properly. 
Because the trajectory is so short the results are moot and should not be compared with the experiment.

```code-block:: bash
   # run the script to extract Dtr
   cd example
   make
```

See the [example_output](example_output)

</div>
