#!/bin/bash

echo "The script starts now:  I expect two files Not_Nulled_Basis.nii and Nulled_Basis_b.nii that are motion corrected with SPM"


echo "temporal upsampling and shifting happens now"

for runNb in {1..4}
do
   echo ""
   echo "run $runNb "
   echo ""


$HOME/abin/3dcalc \
    -a ${output_dir}/moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii'[0..$(2)]' \
    -expr 'a' \
    -prefix ${output_dir}/tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii \
    -overwrite
$HOME/abin/3dcalc \
    -a ${output_dir}/moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_bold.nii'[1..$(2)]' \
    -expr 'a' \
    -prefix ${output_dir}/tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_bold.nii \
    -overwrite

$HOME/abin/3dUpsample \
    -overwrite  \
    -datum short \
    -prefix ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii \
    -n 2 \
    -input ${output_dir}/tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii
$HOME/abin/3dUpsample \
    -overwrite  \
    -datum short \
    -prefix ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_bold.nii \
    -n 2 \
    -input ${output_dir}/tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_bold.nii

NumVol=`$HOME/abin/3dinfo -nv ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_bold.nii`
$HOME/abin/3dTcat \
    -overwrite \
    -prefix ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii \
    ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii'[0]' \
    ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii'[0..'`expr $NumVol - 2`']' 

echo "BOLD correction happens now"
# /Users/barilari/data/tools/LAYNII/LN_BOCO \
    # -Nulled upsmpl_tempco_moco_run${runNb}_4D_vaso.nii \
    # -BOLD upsmpl_tempco_moco_run${runNb}_4D_bold.nii \
    # -trialBOCO 40
$laynii/LN_BOCO \
    -Nulled ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii \
    -BOLD ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_bold.nii


echo "I am correcting for the proper TR in the header"
$HOME/abin/3drefit \
    -TR 2.25 \
    ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_bold.nii
$HOME/abin/3drefit \
    -TR 1.6 \
    ${output_dir}/upsmpl_tempco_moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso_VASO_LN.nii

# run for only run1
echo "calculating T1 in EPI space"
NumVol=`$HOME/abin/3dinfo -nv ${output_dir}/moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii`
$HOME/abin/3dcalc \
    -a ${output_dir}/moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_vaso.nii'[3..'`expr $NumVol - 2`']' \
    -b ${output_dir}/moco_sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_bold.nii'[3..'`expr $NumVol - 2`']' \
    -expr 'a+b' -prefix combined.nii -overwrite
$HOME/abin/3dTstat \
    -cvarinv \
    -prefix ${output_dir}/sub-pilot001_ses-00${ses}_task-${task}_run-00${runNb}_epiT1w.nii \
    -overwrite combined.nii 
rm combined.nii

done

# echo "calculating Mean and tSNR maps"
# $HOME/abin/3dTstat \
#     -mean \
#     -prefix mean_nulled.nii \
#     tempco_moco_run${runNb}_4D_vaso.nii \
#     -overwrite
# $HOME/abin/3dTstat \
#     -mean \
#     -prefix mean_notnulled.nii \
#     tempco_moco_run${runNb}_4D_bold.nii \
#     -overwrite
# $HOME/abin/3dTstat  \
#     -overwrite \
#     -mean  \
#     -prefix BOLD.Mean.nii \
#     upsmpl_tempco_moco_run${runNb}_4D_bold.nii'[1..$]'
# $HOME/abin/3dTstat  \
#     -overwrite \
#     -cvarinv  \
#     -prefix BOLD.tSNR.nii \
#     upsmpl_tempco_moco_run${runNb}_4D_bold.nii'[1..$]'
# $HOME/abin/3dTstat  \
#     -overwrite \
#     -mean  \
#     -prefix VASO.Mean.nii \
#     upsmpl_tempco_moco_run${runNb}_4D_vaso_VASO_LN.nii'[1..$]'
# $HOME/abin/3dTstat  \
#     -overwrite \
#     -cvarinv  \
#     -prefix VASO.tSNR.nii \
#     upsmpl_tempco_moco_run${runNb}_4D_vaso_VASO_LN.nii'[1..$]'

# echo "curtosis and skew"
# /Users/barilari/data/tools/LAYNII/LN_SKEW \
    # -input tempco_moco_run${runNb}_4D_bold.nii
# /Users/barilari/data/tools/LAYNII/LN_SKEW \
    # -input upsmpl_tempco_moco_run${runNb}_4D_vaso_VASO_LN.nii
