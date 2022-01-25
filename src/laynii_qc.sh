#!/usr/bin/env bash

# dataset_path="/Users/barilari/Desktop/data_temp/ses-006_cpp_spm/raw"
# 
# ext='.nii.*'
# 
# is_bids=false
# 
# regex="moco*"${sub_label}"*"${suffix}${ext}"$"
# 
# output_dir=${dataset_path}"/derivatives/laynii/"
# if [ is_bids ];
# then
#     output_dir=${dataset_path}"/derivatives/laynii/"${sub_label}"/func/"
# fi
# 
# mkdir ${output_dir} -p
# 
# file_list=`find ${output_dir} -regex ${regex}`

file_list=$(find "${output_dir}" -name "tempco*.nii")

echo "${file_list}"

for input_file in ${file_list}
do

    # output_basename=`basename ${input_file}`
    # output_file=${output_dir}${output_basename}

    # $laynii/LN_SKEW -input ${input_file} -output ${output_file}

    $laynii/LN_SKEW -input ${input_file}

done

    # save_output_nifti(fout, "skew", nii_skew, true);
    # save_output_nifti(fout, "kurt", nii_kurt, true);
    # save_output_nifti(fout, "autocorr", nii_autocorr, true);
    # save_output_nifti(fout, "mean", nii_mean, true);
    # save_output_nifti(fout, "stedev", nii_stdev, true);
    # save_output_nifti(fout, "tSNR", nii_tSNR, true);
