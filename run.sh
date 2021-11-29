#!/bin/bash

clear

# --- import parameters

source ./src/config.sh

# --- prepare the derivatives folder

# at the moment, it does not copy the files from raw to derivatives -> moved manually

source ./src/prepare_derivative.sh

# --- motion correction

# remember to update `high_res_get_option.m`

/Applications/MATLAB_R2017b.app/bin/matlab -nodesktop -nosplash -r "run('src/motion_correction.m')"

# plot the motion displacement, at the moment it needs more care and one need to provide the path to data inside the script

Rscript ./src/motion_regression.R

# --- QA

suffix="bold"

source ./src/laynii_qc.sh

# --- bold correction

# manually change the nb of runs inside the scripts

source ./src/BOCO.sh

# --- coregistration

# is it better to first run BOCO.sh? This way we have correct for the "missing volumes already", 
# with Remi's refactoring we could run first step 1 and 2 and then coregister and then do bold correction

/Applications/MATLAB_R2017b.app/bin/matlab -nodesktop -nosplash -r "run('src/coregister.m')"

