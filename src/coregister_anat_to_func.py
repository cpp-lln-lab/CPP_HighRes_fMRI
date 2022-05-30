import os
import json
import nibabel as nib


from bids import BIDSLayout

input_folder = (
    "/Users/barilari/data/sandbox_EPI-T1w-layers/outputs/derivatives/cpp_spm-preproc"
)

layout = BIDSLayout(input_folder)

subjectList = layout.get_subjects()

session = "002"

nifti_ext = ".nii"

EPIT1 = layout.get(
    subject="pilot005",
    suffix="T1w",
    space="func",
    extension="nii",
    regex_search=True,
)

path = EPIT1[0].dirname

for subject in subjectList:

    print("\n - Working on subject {} \n".format(subject))

    UNIT1 = layout.get(
        return_type="filename",
        subject=subject,
        suffix="UNIT1",
        desc="skullstripped",
        extension="nii",
        regex_search=True,
    )

    EPIT1 = layout.get(
        return_type="filename",
        subject="pilot005",
        suffix="T1w",
        space="func",
        extension="nii",
        regex_search=True,
    )

    pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}][_task-{task}]_space-individual[_run-{run}]_T1w.nii"

    entities = layout.parse_file_entities(vaso_img[0])
    filename = layout.build_path(entities, pattern, validate=False)

    print("     {}".format(UNIT1[0]))
    print("     {}\n".format(EPIT1[0]))

    # Matthew

    # this argument is taken out
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
        --smoothing-sigmas 3x2x1x0vox"

    os.system(command)

    # Renzo
    command = f"antsRegistration \
        --verbose 1 \
        --dimensionality 3 \
        --float 1 \
        --output [{path}/ANTs_, {path}/ANTs_Warped{nifti_ext},{path}/ANTs_InverseWarped{nifti_ext}] \
        --interpolation Linear \
        --use-histogram-matching 0 \
        --winsorize-image-intensities [0.005,0.995] \
        --transform Rigid[0.05] \
        --metric CC[{EPIT1[0]},{UNIT1[0]},0.7,32,Regular,0.1] \
        --convergence [1000x500,1e-6,10] \
        --shrink-factors 2x1 \
        --smoothing-sigmas 1x0vox \
        --transform Affine[0.1] \
        --metric MI[{EPIT1[0]},{UNIT1[0]},0.7,32,Regular,0.1] \
        --convergence [1000x500,1e-6,10] \
        --shrink-factors 2x1 \
        --smoothing-sigmas 1x0vox \
        --transform SyN[0.1,2,0] \
        --metric CC[{EPIT1[0]},{UNIT1[0]},1,2] \
        --convergence [500x100,1e-6,10] \
        --shrink-factors 2x1 \
        --smoothing-sigmas 1x0vox"

    os.system(command)
