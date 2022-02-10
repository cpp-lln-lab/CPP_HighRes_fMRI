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

    for iVol in volumeIdx[0:-1]:

        print(iVol)

        if (iVol % 2) == 1:

            volumeEvents.append(round(volumeEvents[iVol - 1] + vasoTR, 2))

        else:

            volumeEvents.append(round(volumeEvents[iVol - 1] + boldTR, 2))

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

    newEventsTsv = pd.DataFrame(
        {
            "volumeIdx": volumeIdx,
            "trial_type": volumeType,
            "sequence": volumeList,
            "comulativeTR": volumeEvents,
        }
    )

    print(newEventsTsv)

    fileName = os.path.splitext(file)[0]

    newFileName = fileName + "-volume" + ".tsv"

    print(newFileName)

    newEventsTsv.to_csv(newFileName, sep="\t", index=False)
