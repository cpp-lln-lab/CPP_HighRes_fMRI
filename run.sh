#!/bin/bash

clear

# --- import parameters

source ./src/config.sh

# --- prepare the derivatives folder

# at the moment, it does not copy the files from raw to derivatives -> moved manually, do not copy the events files

source ./src/prepare_derivative.sh

# --- motion correction

# remember to update `high_res_get_option.m`

/Applications/MATLAB_R2017b.app/bin/matlab -nodesktop -nosplash -r "run('src/motion_correction.m')"

# plot the motion displacement, at the moment it needs more care and one need to provide the path to data inside the script

Rscript ./src/motion_regression.R

# TO DO interpolate motion regressors

# --- coregistration

# is it better to first run BOCO.sh? This way we have correct for the "missing volumes already", 
# with Remi's refactoring we could run first step 1 and 2 and then coregister and then do bold correction

/Applications/MATLAB_R2017b.app/bin/matlab -nodesktop -nosplash -r "run('src/coregister.m')"

# --- segment MP2RAGE

# if done in freesurfer this can be done in parallel

# TO DO bias correction in SPM

# TO DO check the paths

recon-all -all -notal-check \
    -s /Users/barilari/Desktop/data_temp/Marco_HighRes/temp/pilot001_no-bias-co_mp2rage \
    -hires \
    -i sub-pilot001_ses-001_acq-hires_UNIT1.nii \
    -expert ./src/expert.opts

# --- bold correction

# manually change the nb of runs inside the scripts

source ./src/BOCO.sh

# --- QA

# run in parallel

# done with the `tempco*` files, the `moco*` ones have missing volumes made of zeros so I supspect it would mess with the math, wouldn't it?

source ./src/laynii_qc.sh

# --- GLM

# this resample and converts the events file from the raw folder, 
# the raw files must be in a "block" version, transormed manually at the moment 
/Applications/MATLAB_R2017b.app/bin/matlab -nodesktop -nosplash -r "run('src/convert_events_tsv.m')"

# this needs to be run twice, one per contrast and you choose which one inside
/Applications/MATLAB_R2017b.app/bin/matlab -nodesktop -nosplash -r "run('src/run_glm.m')"
