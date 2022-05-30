%numRuns=length(dir('S*.nii'));
clear;

path = '/Users/barilari/data/sandbox_EPI-T1w-layers/outputs/derivatives/temp';

fileID = fopen(fullfile(path, 'NT.txt'),'r');

nTRs = fscanf(fileID,'%f');

files=dir(fullfile(path, ['sub-pilot005_ses-002_task-gratingBimodalMotion_run-001_*.nii']));

allFiles=[]; 

allFiles_a=[]; 

allFiles_b=[];

for runs=1:length(files)
    
    nTR=nTRs(runs);
    
    if mod(nTR,2) == 1
        
        nTR=nTR-1; %make it to be even number
    end
    
    if mod(runs,2) ==1  
        
        base=files(runs).name;
        
        for TR= 1:nTR
        
            inst={[base ',' num2str(TR)]};
            
            allFiles_b = [allFiles_b; fullfile(path, inst)]; %#ok<AGROW>
        
        end
        
    elseif mod(runs,2)==0
        
        base=files(runs).name;
        
        for TR= 1:nTR
        
            inst={[base ',' num2str(TR)]};
            
            allFiles_a = [allFiles_a; fullfile(path, inst)]; %#ok<AGROW>
        
        end
        
    end
        
end

allFiles_b = allFiles_b(1:2:end,:);  % odd matrix
allFiles_a = allFiles_a(2:2:end,:);  % even matrix

allFiles_a={allFiles_a};
allFiles_b={allFiles_b};


for bases=1:2
    if bases ==2
        Dataprefix=['Not_Nulled_'];
        allFiles=allFiles_a;
    elseif bases==1
        Dataprefix=['Nulled_'];
        allFiles=allFiles_b;
    end
    matlabbatch{bases}.spm.spatial.realign.estwrite.data = allFiles;  %#ok<*SAGROW>
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.quality = 1;
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.sep = 1.2;
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.fwhm = 1;
% if you want to use the first, use rtm = 0, if you want to use the mean use rtm = 1
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.rtm = 0;
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.interp = 4;
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.wrap = [0 0 0];
    matlabbatch{bases}.spm.spatial.realign.estwrite.eoptions.weight = {''};
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.which = [2 1];
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.interp = 4;
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.wrap = [0 0 0];
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.mask = 1;
    matlabbatch{bases}.spm.spatial.realign.estwrite.roptions.prefix = Dataprefix;
    
end



spm('defaults','FMRI')
spm_jobman('initcfg');
spm_jobman('run',matlabbatch);
















