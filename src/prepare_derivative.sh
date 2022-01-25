#!/bin/bash

# read the files to work with
input_files=$(find "${input_dir}" -name "*_boldcbv.nii")

echo "${input_files}"

# create the destination folder is it does not exists
mkdir -p $output_dir

for input_file in ${input_files}; do
    echo ""
    echo "processing:" "${input_file}"
    echo ""

    # create a tmp name
    output_file="${input_dir}/tmp.nii"

    # duplicate the func image
    cp -v "${input_file}" "${output_file}"

    chmod 777 $output_file

    # remove x nb of dummies cause we are not in steady state just yet
    $afni/3dTcat -prefix "${output_file}" \
        "${output_file}"'['$nb_dummies'..$]' \
        -overwrite

    # duplicate again and move into derivatives
    output_bold=$(echo ${input_file} | sed "s/_boldcbv.nii/_bold.nii/g")
    cp -v "${output_file}" "${output_bold}"
    mv -v "${output_bold}" "${output_dir}"
    output_vaso=$(echo ${input_file} | sed "s/_boldcbv.nii/_vaso.nii/g")
    cp -v "${output_file}" "${output_vaso}"
    mv -v "${output_vaso}" "${output_dir}"

    rm "${output_file}"

done