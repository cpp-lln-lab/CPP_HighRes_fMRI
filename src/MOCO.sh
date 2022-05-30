#!/bin/bash

# ## duplicate the func image
# cp Smagn.nii ./Basis_a.nii

# ## remove 4 dummies cause we are not in steady state just yet
# 3dTcat -prefix Basis_a.nii Basis_a.nii'[4..7]' Basis_a.nii'[4..$]' -overwrite

# ## duplicate again 
# cp ./Basis_a.nii ./Basis_b.nii

## write down the numbers of TR in each image, will be used by SPM
3dinfo -nt sub-pilot005_ses-002_task-gratingBimodalMotion_run-001_bold.nii >> NT.txt
3dinfo -nt sub-pilot005_ses-002_task-gratingBimodalMotion_run-001_vaso.nii >> NT.txt


# NOTE: matlab might be at a different loation on your mashine. 
## run `mocobatch` in matlab
/Applications/MATLAB_R2017b.app/bin/matlab -nodesktop -nosplash -r "mocobatch"

## with Renzo's path
## /Applications/MATLAB_R2018b.app/bin/matlab -nodesktop -nosplash -r "mocobatch"




gnuplot "gnuplot_moco.txt"

#rm ./Basis_*.nii
