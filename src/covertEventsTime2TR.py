import numpy as np
import pandas as pd
import glob
import os

run = 1

# set TRs timings
boldTR = 2.25
vasoTR = 1.6

# set path of the events files to convert
path = "/Users/barilari/data/temp/ses-007_grandmean/sub-pilot001/ses-007/func"

# list the events files
files = glob.glob(path + "/*events.tsv")

print("\n      Will covert this files:")

for file in files:
    print(file)

# loop across the files (runs), convert and write the new file
for file in files:

    ## Read the file and compute run information
    # read the file and save it in a table
    eventsTsv = pd.read_table(file, sep="\t", header=0)

    # compute the end of each event
    offset = np.add(eventsTsv["onset"], eventsTsv["duration"])

    # clean events table and add offset
    eventsTsv["offset"] = offset

    # compute the run duration based on the last event offset, we don't if there are extra volumes
    # so we add 10 seconds more that will be cosidered 'baseline'
    runDuration = offset[len(offset) - 1] + 10

    ## Compute baseline events
    # add baseline for onset delay
    onsetBaseline = [0 + 0.00001]

    durationBaseline = [eventsTsv["onset"][0] - 0.00001]

    offsetBaseline = [eventsTsv["onset"][0] - 0.00001]

    baselineType = "baseline"

    # add baseline for IBI
    for iEvent in range(len(offset[0:-1])):

        onsetBaseline.append(offset[iEvent])

        durationBaseline.append(
            eventsTsv["onset"][iEvent + 1] - offset[iEvent] - 0.00001
        )

        offsetBaseline.append(onsetBaseline[iEvent + 1] + durationBaseline[iEvent + 1])

    # add baseline for end delay
    onsetBaseline.append(offset[len(offset) - 1] + 0.001)

    durationBaseline.append(runDuration - offset[len(offset) - 1])

    offsetBaseline.append(runDuration)

    # create baslein events table
    baselineEvents = pd.DataFrame(
        {
            "onset": onsetBaseline,
            "duration": durationBaseline,
            "trial_type": baselineType,
            "offset": offsetBaseline,
        }
    )

    # merge baseline events to events table
    eventsTsv = pd.concat([eventsTsv, baselineEvents], ignore_index=True)

    eventsTsv = eventsTsv.sort_values(by="onset")

    eventsTsv = eventsTsv.reset_index(drop=True)

    # save the new events file (temporary])
    temp = "~/Desktop/eventsWithBaseline_run-" + str(run) + ".tsv"

    run = run + 1

    eventsTsv.to_csv(temp, sep="\t", index=False)

    ## Compute volume wise events
    # compute the number of vaso + bold volumes
    nbVasoBoldCouple = round(runDuration / (boldTR + vasoTR))

    # make a list of volumes per type of sequence name
    volumeList = ["vaso", "bold"] * nbVasoBoldCouple

    # make a list to index the volume (1 to last volume)
    volumeIdx = list(range(1, len(volumeList) + 1))

    # compute the onset of each volume (TR) starting from zero
    onsetVolumes = [0]

    for iVol in volumeIdx[0:-1]:

        if (iVol % 2) == 1:

            onsetVolumes.append(round(onsetVolumes[iVol - 1] + vasoTR, 2))

        else:

            onsetVolumes.append(round(onsetVolumes[iVol - 1] + boldTR, 2))

        volumeType = []

    # compute offset of each volume (TR) starting from the the onset of the second volume
    offsetVolumes = onsetVolumes[1:]

    if volumeList[-1] == "vaso":

        offsetVolumes.append(offsetVolumes[-1] + vasoTR)

    else:

        offsetVolumes.append(offsetVolumes[-1] + boldTR)

    # compute what stimulation was presented per volume according to the original events file
    iEvent = 0

    trial_type = eventsTsv["trial_type"]

    for iVol in range(len(volumeIdx)):

        if onsetVolumes[iVol] < eventsTsv.iloc[iEvent]["offset"]:

            volumeType.append(eventsTsv["trial_type"].loc[iEvent])

        else:

            iEvent = iEvent + 1

            volumeType.append(eventsTsv["trial_type"].loc[iEvent])

    # tag the volumes (1) in case within a volume acquisiotn the stimulation changed
    volumeChangeStimulation = []

    iOnset = 1

    for iVol in range(len(volumeIdx)):

        if onsetVolumes[iVol] < eventsTsv["onset"].loc[iOnset] < offsetVolumes[iVol]:

            volumeChangeStimulation.append(1)

            if iOnset < len(eventsTsv) - 1:

                iOnset = iOnset + 1

        else:

            volumeChangeStimulation.append(0)

    # tag the volumes, vaso and bold together, (1) which the stimulation for the copule vaso + bold is different
    # (in this case bold correction is meaningless)
    badVasoBOCO = []

    for iVol in range(0, len(volumeIdx), 2):

        if iVol == len(volumeIdx) - 1 and (len(volumeIdx) % 2) == 1:

            badVasoBOCO.append(1)

        if volumeType[iVol + 1] != volumeType[iVol] and volumeList[iVol] == "vaso":

            badVasoBOCO.append(1)
            badVasoBOCO.append(1)

        else:

            badVasoBOCO.append(0)
            badVasoBOCO.append(0)

    newEventsVolumesTsv = pd.DataFrame(
        {
            "volumeIdx": volumeIdx,
            "trial_type": volumeType,
            "sequence": volumeList,
            "onset_TR": onsetVolumes,
            "offset_TR": offsetVolumes,
            "volumeStimulationChange": volumeChangeStimulation,
            "badVasoBOCO": badVasoBOCO,
        }
    )

    fileName = os.path.splitext(file)[0]

    newFileName = fileName + "-volume" + ".tsv"

    newEventsVolumesTsv.to_csv(newFileName, sep="\t", index=False)
