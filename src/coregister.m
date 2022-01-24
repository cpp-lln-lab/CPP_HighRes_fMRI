% (C) Copyright 2021 CPP_High-Res_fMRI developers

clear;
clc;

addpath('../../../srcHighRes')

run ../../CPP_SPM/initCppSpm.m;

%% --- parameters

use_schema = false;

opt = high_res_get_option();


%% coregisterMP2RAGEToT1w

derivativesDir =   opt.derivativesDir;

derivatives = bids.layout(derivativesDir, use_schema);

MP2RAGE = bids.query(derivatives, 'data', ...
                     'sub', opt.subLabel, ...
                     'suffix', 'UNIT1', ...
                     'acq', 'lores', ...
                     'extension', '.nii');

other = bids.query(derivatives, 'data', ...
                   'sub', opt.subLabel, ...
                   'suffix', 'MP2RAGE', ...
                   'acq', 'lores', ...
                   'extension', '.nii');

T1w = bids.query(derivatives, 'data', ...
                 'sub', opt.subLabel, ...
                 'suffix', 'T1w', ...
                 'extension', '.nii');
 
%% coregisterMp2rageToT1w
matlabbatch = {};
matlabbatch = setBatchCoregistration(matlabbatch, T1w{1}, MP2RAGE{1}, other);
batchName = 'coregisterMp2rageToT1w';
saveAndRunWorkflow(matlabbatch, batchName, opt, opt.subLabel);

%% coregisterVasoToT1w
% and also bold and fake T1

derivatives = bids.layout(opt.derivativesDir, use_schema);

mean_bold = bids.query(derivatives, 'data', ...
                       'sub', opt.subLabel, ...
                       'task', opt.task, ...
                       'prefix', 'mean', ...
                       'suffix', 'bold', ...
                       'extension', '.nii');

mean_vaso = bids.query(derivatives, 'data', ...
                       'sub', opt.subLabel, ...
                       'task', opt.task, ...
                       'prefix', 'mean', ...
                       'suffix', 'vaso', ...
                       'extension', '.nii');

other = bids.query(derivatives, 'data', ...
                   'sub', opt.subLabel, ...
                   'task', opt.task, ...
                   'prefix', 'moco_', ...
                   'extension', '.nii');
               
other = cat(1, other, mean_vaso);

matlabbatch = {};
matlabbatch = setBatchCoregistration(matlabbatch, T1w{1}, mean_bold{1}, other);
batchName = 'coregisterVasoToT1w';
saveAndRunWorkflow(matlabbatch, batchName, opt, opt.subLabel);

exit;
