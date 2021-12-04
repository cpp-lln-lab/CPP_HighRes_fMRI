# Segmentation MP2RAGE

## NighRes

It does not work (at list on mine) on a mac, either using docker or the `build` installation.

## Freesurfer

useful links:

- https://surfer.nmr.mgh.harvard.edu/fswiki/SubmillimeterRecon
- https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all#ExpertOptionsFile
- https://surfer.nmr.mgh.harvard.edu/fswiki/HighFieldRecon
- https://layerfmri.com/2017/12/21/bias-field-correction/
- https://www.sciencedirect.com/science/article/abs/pii/S1053811905001102?via%3Dihub

`recon-all -all -s $SUBJECT -hires -i $IMAGE -expert $EXPERT_FILE`

content of the file `experts.opts` is `mris_inflate -n 100`

### Trials

- [ ] run it without bias field correction
  - [x] hi res (error)
  - [x] hi res -notal-check
  - [x] low res
  - [x] low res -notal-check
- [ ] run it with bias field correction
  - [x] low res 20 fwhm
  - [x] low res 60 fwhm

#### trial 1 - local mac no bias field correction

command run

```
recon-all -all -s pilot001_no-bias-co_mp2rage -hires -i sub-pilot001_ses-001_acq-hires_UNIT1.nii -expert /Users/barilari/Desktop/data_temp/Marco_HighRes/temp/expert.opts
```

failed:

from the logfile

```
#--------------------------------------------
#@# Talairach Failure Detection Sun Nov 28 16:37:42 CET 2021
/Applications/freesurfer/subjects/pilot001_no-bias-co_mp2rage/mri
\n talairach_afd -T 0.005 -xfm transforms/talairach.xfm \n
ERROR: talairach_afd: Talairach Transform: transforms/talairach.xfm ***FAILED*** (p=0.0744, pval=0.0034 < threshold=0.0050)
\nManual Talairach alignment may be necessary, or
include the -notal-check flag to skip this test,
making sure the -notal-check flag follows -all
or -autorecon1 in the command string.
See:\n
http://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/Talairach

\nERROR: Talairach failed!\n
Darwin mac-554-749.local 18.7.0 Darwin Kernel Version 18.7.0: Tue Jun 22 19:37:08 PDT 2021; root:xnu-4903.278.70~1/RELEASE_X86_64 x86_64

recon-all -s pilot001_no-bias-co_mp2rage exited with ERRORS at Sun Nov 28 16:37:43 CET 2021

To report a problem, see http://surfer.nmr.mgh.harvard.edu/fswiki/BugReporting

```

This link is suggested above
https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/Talairach


#### trial 2 - local mac no bias field correction

command run

```
recon-all -all -notal-check -s /Users/barilari/Desktop/data_temp/Marco_HighRes/temp/pilot001_no-bias-co_mp2rage -hires -i sub-pilot001_ses-001_acq-hires_UNIT1.nii -expert /Users/barilari/Desktop/data_temp/Marco_HighRes/temp/expert.opts
```

#### trial 3 - monster no bias field correction for `acq-hires`

```
recon-all -all -notal-check -s pilot001_no-bias-co_mp2rage -hires -i sub-pilot001_ses-001_acq-hires_UNIT1.nii -expert /expert.opts
```

#### trial 4 - monster no bias field correction for `acq-lores`

```
recon-all -all -notal-check -s pilot001_no-bias-co_mp2rage -hires -i sub-pilot001_ses-001_acq-hires_UNIT1.nii -expert /expert.opts
```

#### trial 5 - monster no bias field correction for `acq-lores` and without talairach constriction

```
export FREESURFER_HOME=/usr/local/freesurfer/7.2.0-1
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export SUBJECTS_DIR=/home/marcobar/Data/data_temp/mp2rage

recon-all -all -s monster_biasCo-no_pilot001_acq-lores_mp2rage -hires -i sub-pilot001_ses-001_acq-lores_UNIT1.nii -expert expert.opts
```
#### trial 6 - monster no bias field correction for `acq-hires` and without talairach constriction

```
export FREESURFER_HOME=/usr/local/freesurfer/7.2.0-1
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export SUBJECTS_DIR=/home/marcobar/Data/data_temp/mp2rage

recon-all -all -s monster_biasCo-no_pilot001_acq-hires_mp2rage -hires -i sub-pilot001_ses-001_acq-hires_UNIT1.nii -expert expert.opts
```

same error as trial 1

```
#--------------------------------------------
#@# Talairach Failure Detection Wed Dec  1 17:59:18 CET 2021
/home/marcobar/Data/data_temp/mp2rage/monster_biasCo-no_pilot001_acq-hires_mp2rage/mri

 talairach_afd -T 0.005 -xfm transforms/talairach.xfm

ERROR: talairach_afd: Talairach Transform: transforms/talairach.xfm ***FAILED*** (p=0.0503, pval=0.0034 < threshold=0.0050)
@#@FSTIME  2021:12:01:17:59:18 talairach_afd N 4 e 0.01 S 0.00 U 0.00 P 80% M 2576 F 0 R 728 W 0 c 1 w 1 I 0 O 0 L 2.64 4.00 5.78
@#@FSLOADPOST 2021:12:01:17:59:18 talairach_afd N 4 2.64 4.00 5.78

Manual Talairach alignment may be necessary, or
include the -notal-check flag to skip this test,
making sure the -notal-check flag follows -all
or -autorecon1 in the command string.
See:

http://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/Talairach


ERROR: Talairach failed!

Linux 1075.psp.ucl.ac.be 3.10.0-1160.42.2.el7.x86_64 #1 SMP Tue Sep 7 14:49:57 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux

recon-all -s monster_biasCo-no_pilot001_acq-hires_mp2rage exited with ERRORS at Wed Dec  1 17:59:18 CET 2021

For more details, see the log file /home/marcobar/Data/data_temp/mp2rage/monster_biasCo-no_pilot001_acq-hires_mp2rage/scripts/recon-all.log
To report a problem, see http://surfer.nmr.mgh.harvard.edu/fswiki/BugReporting
```

#### trial 7 - monster with bias field at `biasfwhm = 20` correction for `acq-lores` and without talairach constriction

```
export FREESURFER_HOME=/usr/local/freesurfer/7.2.0-1
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export SUBJECTS_DIR=/home/marcobar/Data/data_temp/mp2rage

recon-all -all -s monster_biasCo-20fwhm_pilot001_acq-lores_mp2rage -hires -i msub-pilot001_ses-001_acq-lores_fwhm-20_UNIT1.nii -expert expert.opts
```

#### trial 8 - monster with bias field at `biasfwhm = 60` correction for `acq-lores` and without talairach constriction

```
export FREESURFER_HOME=/usr/local/freesurfer/7.2.0-1
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export SUBJECTS_DIR=/home/marcobar/Data/data_temp/mp2rage

recon-all -all -s monster_biasCo-60fwhm_pilot001_acq-lores_mp2rage -hires -i msub-pilot001_ses-001_acq-lores_fwhm-60_UNIT1.nii -expert expert.opts
```
