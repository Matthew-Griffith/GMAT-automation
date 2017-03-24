'''
This script will take the reports created by GMAT from running
script_automation.bat file and find the time the two satellites stay within
1 km of each other for each report. then, it will compile this info into a .csv
with the parameters that were varied. these varied parameters will be found by
using the filename which has the following convention...

Date_Time_radiusPeriasis_Eccentricity_Inclination_sepVelV_sepVelN_sepVelB.csv
'''

# this function will return a list of filename given a path to a directory
from os import listdir
# this module will make dealing with csv files easier.
import csv
from math import sqrt
import re

pathReport = "C:/Users/mattg/Documents/GitHub/GMAT-automation/GMAT-Reports/"
fileNameReports = listdir(pathReport)

'''
now we need to loop through every file in our reports directory, and load the
columns of the csv report files into memory find the distance and add up the
time they are with in 1 km. recall that the reports a column structure of...

Emitter X pos, Emitter y pos, Emitter z pos, Detector X pos, Detector y pos, Detector z pos, time
'''

time1kmList = []
for i in range(len(fileNameReports)):
    with open(pathReport + fileNameReports[i]) as currentReport:
        reportData = csv.reader(currentReport, delimiter = ',')

        # now that we have the files with the report directory opening and the
        # csv data is loaded into memory we want to create some empry lists that
        # we will store data to
        emitterPosX = []
        emitterPosY = []
        emitterPosZ = []
        detectorPosX = []
        detectorPosY = []
        detectorPosZ = []
        time = []

        # now we can loop through our csv data and save the values into temp vars
        # and append them to these list.
        for row in reportData:
            tempEmitterX = row[0]
            tempEmitterY = row[1]
            tempEmitterZ = row[2]
            tempDetectorX = row[3]
            tempDetectorY = row[4]
            tempDetectorZ = row[5]
            tempTime = row[6]
            emitterPosX.append(tempEmitterX)
            emitterPosY.append(tempEmitterY)
            emitterPosZ.append(tempEmitterZ)
            detectorPosX.append(tempDetectorX)
            detectorPosY.append(tempDetectorY)
            detectorPosZ.append(tempDetectorZ)
            time.append(tempTime)

        # now that we have data saved from the csv we need to convert it from
        # strings to floats.
        emitterPosX = list(map(float, emitterPosX))
        emitterPosY = list(map(float, emitterPosY))
        emitterPosZ = list(map(float, emitterPosZ))
        detectorPosX = list(map(float, detectorPosX))
        detectorPosY = list(map(float, detectorPosY))
        detectorPosZ = list(map(float, detectorPosZ))
        time = list(map(float, time))

        for j in range(len(time)):
            distance = sqrt((emitterPosX[j] - detectorPosX[j])**2 +
                             (emitterPosY[j] - detectorPosY[j])**2 +
                             (emitterPosZ[j] - detectorPosZ[j])**2)
            # here on the first iteration of each loop we either create or
            # reset the var time1km this is important for the elif statement
            # below so it will not try to access [-1]
            if j == 0:
                time1km = 0
            elif distance <= 1:
                time1km += (time[j] - time[j-1])
            else:
                pass

        time1kmList.append(time1km)

'''
now that we have time the two satellites are within 1 km of each I want to save
this info with the parameters that we varied with GMAT to another .csv file.
recall from the top of this file that the filename of the reports actually
contain these parameters that were used in GMAT. And we have a list of the time
so we can go through the time and write each row of a csv file where the first
several columns tell the gmat parameters and the last one is the result.

however, before this I want to write a header for column.
'''
with open('C:/Users/mattg/Documents/GitHub/GMAT-automation/results/all_results.csv', 'w', newline = '') as csvfile:
    resultsWriter = csv.writer(csvfile, delimiter = ',')
    resultsWriter.writerow(['Month', 'Hour', 'Radius of Periapsis [km]', 'Eccentricity',
                            'inclination', 'separation velocity V [km/s]',
                            'separation velocity N [km/s]', 'separation velocity B [km/s]',
                            'Time to 1 km [secs]'])

    # now that we have our header line we can start looping and writing the
    # rest of the file.
    for j in range(len(time1kmList)):
        # since we want to write the times to a file we need to convert from
        # floats to strings.
        time1kmListStr = list(map(str, time1kmList))
        # next we want to grab the gmat variables from the filename, these are
        # all separated by underscores (_)
        currentRow = fileNameReports[j].split('_')
        # however, the last entry will have a .csv that we want to remove.
        currentRow[7] = re.sub(r'\.csv$', '', currentRow[7])
        currentRow.append(time1kmListStr[j])
        resultsWriter.writerow(currentRow)
