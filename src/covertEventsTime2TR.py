import numpy as np
import pandas as pd

boldTR = 2.25
vasoTR = 1.6

eventsTsv = pd.read_table('/Users/barilari/data/temp_to_delete/ses-007_bold-classic-noInterp/derivatives/cpp_spm-preproc/sub-pilot001/ses-007/func/sub-pilot001_ses-007_task-visualLocalizerFingerTapping_run-001_events.tsv', sep='\t', header=0)

end = np.add(eventsTsv["onset"], eventsTsv["duration"])

eventsTsv["end"] = end




# -------------------------------------------------------------------------------------

# mockEventsStarts = [5.064472,	35.536482,	65.939492,	96.094513,	126.47973,	156.608455,	187.015942]

# mockDuration = [28.336928, 28.277807, 28.032229, 28.262789,	28.009508, 28.284508, 28.017616] 

# mockTrialType = [ 'static', 'motion' ] * len(mockEventsStarts)

mockEventsEnd = np.add(mockEventsStarts, mockDuration)

runDuration = mockEventsEnd[len(mockEventsEnd)-1]

nbVasoBoldCouple = round(runDuration / (boldTR + vasoTR))

volumeList = [ 'vaso', 'bold' ] * nbVasoBoldCouple

volumeIdx = list(range(1, len(volumeList)+1))

volumeEvents = [ 0 ]

for iVol in volumeIdx:

  print(iVol)
    
  if (iVol % 2) == 1:

      volumeEvents.append(round(volumeEvents[iVol - 1] + vasoTR, 2)) 

  else:

      volumeEvents.append(round(volumeEvents[iVol - 1] + boldTR, 2)) 

print(volumeEvents)

volumeType = []

iTime = 0

for iVol in range(len(volumeIdx)):

    if volumeEvents[iVol] < mockEventsEnd[iTime]:

        volumeType.append(mockTrialType[iTime])

    else:
  
        iTime = iTime +1

        volumeType.append(mockTrialType[iTime])

    print('{} within {} then {}'.format(volumeEvents[iVol], mockEventsEnd[iTime], mockTrialType[iTime]))
    print('volume: {}; event {}'.format(iVol, iTime))

 