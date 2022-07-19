import os
import json
import nibabel as nib
from nibabel.processing import resample_to_output
from bids import BIDSLayout

input_folder = (
    "/Users/barilari/data/sandbox_EPI-T1w-layers/outputs/derivatives/cpp_spm-preproc"
)

layout = BIDSLayout(input_folder)

# subjectList = layout.get_subjects()

subjectList = "pilot001"

session = "001"

nifti_ext = ".nii"

UNIT1 = layout.get(
    subject=subjectList,
    suffix="UNIT1",
    acquisition="r0p375",
    desc="skullstripped",
    extension="nii",
    regex_search=True,
)

path = UNIT1[0].dirname

for subject in subjectList:

    print("\n - Working on subject {} \n".format(subject))

    UNIT1 = layout.get(
        return_type="filename",
        subject=subject,
        suffix="UNIT1",
        acquisition="r0p375",
        desc="skullstripped",
        extension="nii",
        regex_search=True,
    )

    EPIT1 = layout.get(
        return_type="filename",
        subject=subject,
        suffix="T1w",
        space="func",
        extension="nii",
        regex_search=True,
    )

    MTmask = layout.get(
        return_type="filename",
        subject=subject,
        suffix="mask",
        label="MT",
        space="funcSes002",
        extension="nii",
        regex_search=True,
    )

    PTmask = layout.get(
        return_type="filename",
        subject=subject,
        suffix="mask",
        label="PT",
        space="funcSes002",
        extension="nii",
        regex_search=True,
    )

    pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}]_space-EPIT1w_label-MT_acq-r0p375_UNIT1.nii"

    entities = layout.parse_file_entities(UNIT1[0])
    filename = layout.build_path(entities, pattern, validate=False)

    print("     {}".format(UNIT1[0]))
    print("     {}\n".format(EPIT1[0]))
    print("     {}\n".format(MTmask[0]))
    print("     {}\n".format(PTmask[0]))

    # MT

    # this argument is taken out since the two images are already coregistered
    # --initial-moving-transform {T2w_to_func_init} \

    command = f"antsRegistration \
        --verbose 1 \
        --dimensionality 3 \
        --float 0 \
        --output [{path}/ANTs_, {path}/ANTs_Warped{nifti_ext},{path}/ANTs_InverseWarped{nifti_ext}] \
        --interpolation Linear \
        --use-histogram-matching 0 \
        --winsorize-image-intensities [0.005,0.995] \
        --transform Rigid[0.05] \
        --metric MI[{EPIT1[0]},{UNIT1[0]},0.7,32,Regular,0.1] \
        --convergence [1000x500,1e-6,10] \
        --shrink-factors 2x1 \
        --smoothing-sigmas 1x0vox \
        --transform Affine[0.1] \
        --metric MI[{EPIT1[0]},{UNIT1[0]},0.7,32,Regular,0.1] \
        --convergence [1000x500,1e-6,10] \
        --shrink-factors 2x1 \
        --smoothing-sigmas 1x0vox \
        --transform SyN[0.1,3,0] \
        --metric CC[{EPIT1[0]},{UNIT1[0]},1,4] \
        --convergence [100x70x50x20,1e-6,10] \
        --shrink-factors 4x4x2x1 \
        --smoothing-sigmas 3x2x1x0vox \
        -x {MTmask[0]}"

    os.system(command)

    ## RESLICE WITH SPM

    layout = BIDSLayout(input_folder)

    # UNIT1MTmoved = layout.get(
    #     return_type="filename",
    #     subject=subject,
    #     suffix="UNIT1",
    #     acquisition="r0p375",
    #     space="EPIT1w",
    #     label="MT",
    #     extension="nii",
    #     regex_search=True,
    # )

    EPIT1usampled = layout.get(
        return_type="filename",
        subject=subject,
        suffix="T1w",
        space="func",
        acquisition="r0p375",
        extension="nii",
        regex_search=True,
    )

    LAYERS = layout.get(
        return_type="filename",
        subject=subject,
        suffix="equivol",
        extension="nii",
        regex_search=True,
    )

    MTxfm = layout.get(
        return_type="filename",
        subject=subject,
        acquisition="r0p375",
        label="MT",
        suffix="xfm",
        extension="nii",
        regex_search=True,
    )

    MTgenericAffine = layout.get(
        return_type="filename",
        subject=subject,
        suffix="xfm",
        label="MT",
        extension="mat",
        regex_search=True,
    )

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_space-EPIT1w_label-6layerMTw_mask_layers_equivol.nii"
    entities = layout.parse_file_entities(LAYERS[0])
    filename = layout.build_path(entities, pattern, validate=False)

    command = f"antsApplyTransforms \
        --interpolation NearestNeighbor \
        --dimensionality 3 \
        --input {LAYERS[0]} \
        --reference-image {EPIT1usampled[0]} \
        --transform {MTxfm[0]} \
        --transform {MTgenericAffine} \
        --output {filename}"

    os.system(command)

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_hemi-R_space-EPIT1w_label-MT_mask.nii"
    entities = layout.parse_file_entities(MTmask[0])
    filename = layout.build_path(entities, pattern, validate=False)

    command = f"antsApplyTransforms \
        --interpolation NearestNeighbor \
        --dimensionality 3 \
        --input {MTmask[0]} \
        --reference-image {EPIT1usampled[0]} \
        --transform {MTxfm[0]} \
        --transform {MTgenericAffine} \
        --output {filename}"

    os.system(command)

    # PT

    # this argument is taken out since the two images are already coregistered
    # --initial-moving-transform {T2w_to_func_init} \

    command = f"antsRegistration \
        --verbose 1 \
        --dimensionality 3 \
        --float 0 \
        --output [{path}/ANTs_PT_, {path}/ANTs_Warped_PT{nifti_ext},{path}/ANTs_InverseWarped_PT{nifti_ext}] \
        --interpolation Linear \
        --use-histogram-matching 0 \
        --winsorize-image-intensities [0.005,0.995] \
        --transform Rigid[0.05] \
        --metric MI[{EPIT1[0]},{UNIT1[0]},0.7,32,Regular,0.1] \
        --convergence [1000x500,1e-6,10] \
        --shrink-factors 2x1 \
        --smoothing-sigmas 1x0vox \
        --transform Affine[0.1] \
        --metric MI[{EPIT1[0]},{UNIT1[0]},0.7,32,Regular,0.1] \
        --convergence [1000x500,1e-6,10] \
        --shrink-factors 2x1 \
        --smoothing-sigmas 1x0vox \
        --transform SyN[0.1,3,0] \
        --metric CC[{EPIT1[0]},{UNIT1[0]},1,4] \
        --convergence [100x70x50x20,1e-6,10] \
        --shrink-factors 4x4x2x1 \
        --smoothing-sigmas 3x2x1x0vox \
        -x {PTmask[0]}"

    os.system(command)

    layout = BIDSLayout(input_folder)

    # UNIT1MTmoved = layout.get(
    #     return_type="filename",
    #     subject=subject,
    #     suffix="UNIT1",
    #     acquisition="r0p375",
    #     space="EPIT1w",
    #     label="PT",
    #     extension="nii",
    #     regex_search=True,
    # )

    EPIT1usampled = layout.get(
        return_type="filename",
        subject=subject,
        suffix="T1w",
        space="func",
        acquisition="r0p375",
        extension="nii",
        regex_search=True,
    )

    LAYERS = layout.get(
        return_type="filename",
        subject=subject,
        suffix="equivol",
        space="individual",
        extension="nii",
        regex_search=True,
    )

    PTxfm = layout.get(
        return_type="filename",
        subject=subject,
        acquisition="r0p375",
        label="PT",
        suffix="xfm",
        extension="nii",
        regex_search=True,
    )

    PTgenericAffine = layout.get(
        return_type="filename",
        subject=subject,
        suffix="xfm",
        label="PT",
        extension="mat",
        regex_search=True,
    )

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_space-EPIT1w_label-6layerPTw_mask_layers_equivol.nii"
    entities = layout.parse_file_entities(LAYERS[0])
    filename = layout.build_path(entities, pattern, validate=False)

    command = f"antsApplyTransforms \
        --interpolation NearestNeighbor \
        --dimensionality 3 \
        --input {LAYERS[0]} \
        --reference-image {EPIT1usampled[0]} \
        --transform {PTxfm[0]} \
        --transform {PTgenericAffine} \
        --output {filename}"

    os.system(command)

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_hemi-R_space-EPIT1w_label-PT_mask.nii"
    entities = layout.parse_file_entities(PTmask[0])
    filename = layout.build_path(entities, pattern, validate=False)

    command = f"antsApplyTransforms \
        --interpolation NearestNeighbor \
        --dimensionality 3 \
        --input {PTmask[0]} \
        --reference-image {EPIT1usampled[0]} \
        --transform {PTxfm[0]} \
        --transform {PTgenericAffine} \
        --output {filename}"

    os.system(command)
