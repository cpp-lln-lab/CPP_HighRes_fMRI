
nifti_ext=.nii.gz

# T2w_to_func_init={nifti_dir}T2w_to_func_CC_Affine.txt

st_im={nifti_dir}sub-{sub_id}_run-01_bold_mean

mv_im={nifti_dir_anat}{T2w_name}_skullstrip_upsample0p4

antsRegistration \
        --verbose 1 \
        --dimensionality 3 \
        --float 0 \
        --output [ANTs_, ANTs_Warped{nifti_ext},ANTs_InverseWarped{nifti_ext}] \
        --interpolation Linear \
        --use-histogram-matching 0 \
        --winsorize-image-intensities [0.005,0.995] \
        # --initial-moving-transform {T2w_to_func_init} \
        --transform Rigid[0.05] \
        --metric MI[{st_im}{nifti_ext},{mv_im}{nifti_ext},0.7,32,Regular,0.1] \
        --convergence [1000x500,1e-6,10] \
        --shrink-factors 2x1 \
        --smoothing-sigmas 1x0vox \
        --transform Affine[0.1] \
        --metric MI[{st_im}{nifti_ext},{mv_im}{nifti_ext},0.7,32,Regular,0.1] \
        --convergence [1000x500,1e-6,10] \
        --shrink-factors 2x1 \
        --smoothing-sigmas 1x0vox \
        --transform SyN[0.1,3,0] \
        --metric CC[{st_im}{nifti_ext},{mv_im}{nifti_ext},1,4] \
        --convergence [100x70x50x20,1e-6,10] \
        --shrink-factors 4x4x2x1 \
        --smoothing-sigmas 3x2x1x0vox

