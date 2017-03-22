'''
This script will take the reports created by GMAT from running
script_automation.bat file and find the time the two satellites stay within
1 km of each other for each report. then, it will compile this info into a .csv
with the parameters that were varied. these varied parameters will be found by
using the filename which has the following convention...

Date_Time_semiMajorAxis_Eccentricity_Inclination_sepVelV_sepVelN_sepVelB.csv
'''

# this function will return a list of filename given a path to a directory
from os import listdir
# this module will make dealing with csv files easier.
import csv
from math import sqrt

pathReport = "C:/Users/mattg/Documents/GitHub/GMAT-automation/GMAT-Reports"
fileNameReports = listdir(pathReport)

'''
now we need to loop through every file in our reports directory, and load the
columns of the csv report files into memory find the distance and add up the
time they are with in 1 km. recall that the reports a column structure of...

Emitter X pos, Emitter y pos, Emitter z pos, Detector X pos, Detector y pos, Detector z pos, time
'''

time1kmList = []
for i in range(len(fileNameReports)):
    with open(fileNameReports[i]) as currentReport:
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
        for row in readData:
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

        time1km = 0
        for j in range(len(time)):
            distance = sqrt((emitterPosX[j] - detectorPosX[j])**2 +
                             (emitterPosY[j] - detectorPosY[j])**2 +
                             (emitterPosZ[j] - detectorPosZ[j])**2)
            if j == 0:
                pass
            elif distance <= 1:
                time1km += (time[j] - time[j-1])
            else:
                pass

        time1kmList.append(time1km)

print(time1kmList)
