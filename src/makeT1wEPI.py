import os
import json
import nibabel as nib


from bids import BIDSLayout

input_folder = (
    "/Users/barilari/data/sandbox_EPI-T1w-layers/outputs/derivatives/cpp_spm-preproc"
)

layout = BIDSLayout(input_folder)

# subjectList = layout.get_subjects()
subject = "pilot001"
session = "008"

vaso_run1 = layout.get(
    subject=subject,
    suffix="vaso",
    run="001",
    desc="preproc",
    extension="nii",
    regex_search=True,
)

path = vaso_run1[0].dirname

# for subject in subjectList:

print("\n - Working on subject {} \n".format(subject))

for run in layout.get_runs(subject=subject):

    print("      run nb: {} \n".format(run))

    bold_img = layout.get(
        return_type="filename",
        subject=subject,
        run=run,
        suffix="bold",
        desc="preproc",
        extension="nii",
        regex_search=True,
    )

    vaso_img = layout.get(
        return_type="filename",
        subject=subject,
        run=run,
        suffix="vaso",
        desc="preproc",
        extension="nii",
        regex_search=True,
    )

    print("     {}".format(bold_img[0]))
    print("     {}\n".format(vaso_img[0]))

    vaso_hdr = nib.load(vaso_img[0])

    nb_vol = vaso_hdr.shape[3]

    nb_vol_min2 = nb_vol - 2

    command = f'echo "calculating T1 in EPI space"'

    os.system(command)

    command = f'$HOME/abin/3dcalc \
                -a {vaso_img[0]}"[3..{nb_vol_min2}]" \
                -b {bold_img[0]}"[3..{nb_vol_min2}]" \
                -expr "a+b" -prefix {path}/combined.nii -overwrite'

    os.system(command)

    pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}][_task-{task}]_space-individual[_run-{run}]_T1w.nii"

    entities = layout.parse_file_entities(vaso_img[0])
    filename = layout.build_path(entities, pattern, validate=False)

    command = f"$HOME/abin/3dTstat \
                    -cvarinv \
                    -prefix {filename} \
                    -overwrite {path}/combined.nii"

    os.system(command)

    command = f"rm {path}/combined.nii"

    os.system(command)
