import os
import json
import nibabel as nib
from nibabel.processing import resample_to_output
from bids import BIDSLayout

input_folder = (
    "/Users/barilari/data/sandbox_EPI-T1w-layers/outputs/derivatives/cpp_highres-epiT1w"
)

subjectList = ["pilot001"]

session = "001"

nifti_ext = ".nii"

layout = BIDSLayout(input_folder)

# subjectList = layout.get_subjects()

UNIT1 = layout.get(
    subject=subjectList[0],
    suffix="UNIT1",
    acquisition="r0p375",
    desc="skullstripped",
    extension="nii",
    regex_search=True,
)

path = UNIT1[0].dirname

for subject in subjectList:

    ## RESLICE WITH SPM

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

    # LAYERS = layout.get(
    #     return_type="filename",
    #     subject=subject,
    #     suffix="equivol",
    #     extension="nii",
    #     regex_search=True,
    # )

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

    MTmask = layout.get(
        return_type="filename",
        subject=subject,
        suffix="mask",
        label="rightMTP",
        extension="nii",
        regex_search=True,
    )

    MTa = layout.get(
        return_type="filename",
        subject=subject,
        suffix="mask",
        label="rightMTA",
        extension="nii",
        regex_search=True,
    )

    # ASEGRIM = layout.get(
    #     return_type="filename",
    #     subject=subject,
    #     space="individual",
    #     suffix="rim",
    #     regex_search=True,
    # )

    # pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_space-EPIT1w_label-6layerMTw_mask_layers_equivol.nii"
    # entities = layout.parse_file_entities(LAYERS[0])
    # filename = layout.build_path(entities, pattern, validate=False)

    # command = f"antsApplyTransforms \
    #     --interpolation NearestNeighbor \
    #     --dimensionality 3 \
    #     --input {LAYERS[0]} \
    #     --reference-image {EPIT1usampled[0]} \
    #     --transform {MTxfm[0]} \
    #     --transform {MTgenericAffine} \
    #     --output {filename}"

    # os.system(command)

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_hemi-R_space-EPIT1w_label-rightMTP_mask.nii"
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

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_hemi-R_space-EPIT1w_label-rightMTA_mask.nii"
    entities = layout.parse_file_entities(MTa[0])
    filename = layout.build_path(entities, pattern, validate=False)

    command = f"antsApplyTransforms \
        --interpolation NearestNeighbor \
        --dimensionality 3 \
        --input {MTa[0]} \
        --reference-image {EPIT1usampled[0]} \
        --transform {MTxfm[0]} \
        --transform {MTgenericAffine} \
        --output {filename}"

    os.system(command)

    # pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}]_acq-r0p375_space-EPIT1w_desc-freesurferaseg_label-MTw_rim.nii"
    # entities = layout.parse_file_entities(ASEGRIM[0])
    # filename = layout.build_path(entities, pattern, validate=False)

    # command = f"antsApplyTransforms \
    #     --interpolation NearestNeighbor \
    #     --dimensionality 3 \
    #     --input {ASEGRIM[0]} \
    #     --reference-image {EPIT1usampled[0]} \
    #     --transform {MTxfm[0]} \
    #     --transform {MTgenericAffine} \
    #     --output {filename}"

    # os.system(command)

    # PT

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

    PTmask = layout.get(
        return_type="filename",
        subject=subject,
        suffix="mask",
        label="rightPT",
        extension="nii",
        regex_search=True,
    )

    FP = layout.get(
        return_type="filename",
        subject=subject,
        suffix="mask",
        label="rightFP",
        extension="nii",
        regex_search=True,
    )

    vPTvis = layout.get(
        return_type="filename",
        subject=subject,
        suffix="mask",
        label="rightVentralPTV",
        extension="nii",
        regex_search=True,
    )

    lPTvis = layout.get(
        return_type="filename",
        subject=subject,
        suffix="mask",
        label="rightLateralPTV",
        extension="nii",
        regex_search=True,
    )

    # pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_space-EPIT1w_label-6layerPTw_mask_layers_equivol.nii"
    # entities = layout.parse_file_entities(LAYERS[0])
    # filename = layout.build_path(entities, pattern, validate=False)

    # command = f"antsApplyTransforms \
    #     --interpolation NearestNeighbor \
    #     --dimensionality 3 \
    #     --input {LAYERS[0]} \
    #     --reference-image {EPIT1usampled[0]} \
    #     --transform {PTxfm[0]} \
    #     --transform {PTgenericAffine} \
    #     --output {filename}"

    # os.system(command)

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_hemi-R_space-EPIT1w_label-rightPT_mask.nii"
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

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_hemi-R_space-EPIT1w_label-rightFP_mask.nii"
    entities = layout.parse_file_entities(FP[0])
    filename = layout.build_path(entities, pattern, validate=False)

    command = f"antsApplyTransforms \
        --interpolation NearestNeighbor \
        --dimensionality 3 \
        --input {FP[0]} \
        --reference-image {EPIT1usampled[0]} \
        --transform {PTxfm[0]} \
        --transform {PTgenericAffine} \
        --output {filename}"

    os.system(command)

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_hemi-R_space-EPIT1w_label-rightLateralPTV_mask.nii"
    entities = layout.parse_file_entities(lPTvis[0])
    filename = layout.build_path(entities, pattern, validate=False)

    command = f"antsApplyTransforms \
        --interpolation NearestNeighbor \
        --dimensionality 3 \
        --input {lPTvis[0]} \
        --reference-image {EPIT1usampled[0]} \
        --transform {PTxfm[0]} \
        --transform {PTgenericAffine} \
        --output {filename}"

    os.system(command)

    pattern = "sub-{subject}[/ses-{session}]/roi/sub-{subject}[_ses-{session}]_acq-r0p375_hemi-R_space-EPIT1w_label-rightVentralPTV_mask.nii"
    entities = layout.parse_file_entities(vPTvis[0])
    filename = layout.build_path(entities, pattern, validate=False)

    command = f"antsApplyTransforms \
        --interpolation NearestNeighbor \
        --dimensionality 3 \
        --input {vPTvis[0]} \
        --reference-image {EPIT1usampled[0]} \
        --transform {PTxfm[0]} \
        --transform {PTgenericAffine} \
        --output {filename}"

    os.system(command)

    # pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}]_acq-r0p375_space-EPIT1w_desc-freesurferaseg_label-PTw_rim.nii"
    # entities = layout.parse_file_entities(ASEGRIM[0])
    # filename = layout.build_path(entities, pattern, validate=False)

    # command = f"antsApplyTransforms \
    #     --interpolation NearestNeighbor \
    #     --dimensionality 3 \
    #     --input {ASEGRIM[0]} \
    #     --reference-image {EPIT1usampled[0]} \
    #     --transform {PTxfm[0]} \
    #     --transform {PTgenericAffine} \
    #     --output {filename}"

    # os.system(command)
