#!/bin/bash

# set paths for data
input_dir=../inputs/raw/sub-xxx/ses-xxx/func

output_dir=../outputs/derivatives/cpp_high-res_fmri/sub-pilotxxx/ses-xxx/func

# set paths for the softwares (if not already exported by default in .bash_profife or .bashrc)
afni=$HOME/abin
laynii=$HOME/LAYNII
cpp_highres_fmri=./lib/CPP_High-Res_fMRI/src

# set dataset to analyses information
sub_label=""

task=""

nb_runs=

ses=

nb_dummies=4
bold_tr=2.25
vaso_tr=1.6

suffixes="vaso bold"

first_vol_vaso=1
first_vol_bold=0;
