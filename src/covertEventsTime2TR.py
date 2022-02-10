import numpy as np
import pandas as pd
import glob
import os


boldTR = 2.25
vasoTR = 1.6

path = "/Users/barilari/data/temp_to_delete/ses-007_bold-classic-noInterp/derivatives/cpp_spm-preproc/sub-pilot001/ses-007/func/"

files = glob.glob(path + "/*events.tsv")

print("\n      Will covert this files:")

for file in files:
    print(file)

for file in files:

    eventsTsv = pd.read_table(file, sep="\t", header=0)

    offset = np.add(eventsTsv["onset"], eventsTsv["duration"])

    runDuration = offset[len(offset) - 1]

    nbVasoBoldCouple = round(runDuration / (boldTR + vasoTR))

    volumeList = ["vaso", "bold"] * nbVasoBoldCouple

    volumeIdx = list(range(1, len(volumeList) + 1))

    volumeEvents = [0]

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

            if volumeEvents[iVol] < offset[iTime]:

                volumeType.append(eventsTsv["trial_type"][iTime])

            else:

                iTime = iTime + 1

                volumeType.append(eventsTsv["trial_type"][iTime])

    print(
        "{} within {} then {}".format(
            volumeEvents[iVol], offset[iTime], eventsTsv["trial_type"][iTime]
        )
    )
    print("volume: {}; event {}".format(iVol, iTime))
# -------------------------------------------------------------------------------------

# mockEventsStarts = [5.064472,	35.536482,	65.939492,	96.094513,	126.47973,	156.608455,	187.015942]

# mockDuration = [28.336928, 28.277807, 28.032229, 28.262789,	28.009508, 28.284508, 28.017616]

# mockTrialType = [ 'static', 'motion' ] * len(mockEventsStarts)

# mockEventsEnd = np.add(mockEventsStarts, mockDuration)
