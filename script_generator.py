'''this program will be used to incremental change parameters from the template.script
file and save them to their own file. this will allow us to generate gmat script
files over the range of parameters that can be defined below.'''

from math import sin, cos, pi

# here we will define the range of dates and times to test the simulation over.
dateRange = ["01 Mar 2016", "01 Jun 2016", "01 Sep 2016", "01 Dec 2016"]
timeRange = ["00:00:00.000", "12:00:00.000"]

def float_range(start, stop, step):
    '''python built in range() function doesn't work of floating point numbers.
    this is a simple function that loop saving your changing start value that will be
    incremented by your step value.
    note that to store the values in a list you have to use list()
    ex: list(float_range(1.0, 2.0, 0.1))'''
    while start < stop:
        yield start
        start += step

# here we describe the range of state vector components for a keplarian state vector.
semiMajorAxisRange = list(float_range(6728.137, 6978.137, 50))  # kilometers
eccentricityRange = list(float_range(0.0, 0.9, 0.1))
inclinationRange = [28, 51.6]       # inclination of ksc and ISS

'''below defines the range for separation velocity vector note that the gmat script
performs this separation using the VNB coordination system where...
V (velocity) is in the direction of the velocity vector for the satllite
N (normal) is normal to the orbit plane
B (biNormal) is 90 degress from V & N pointing away from the origin (earth in our case)

first, we will define a range for the intended orientation of the separation velocity.
second, second we account of errors that could occur in the magnitdue and pointing
of the combined satellites.'''

# here we set the range of the orientations using two angles
angleFromNormalAxis = list(float_range(0, pi, pi/3))         # in rad
angleFromVelAxis = list(float_range(0, 2*pi, pi/3))          # in rad
# from here we set the variations of the velocity magnitude
sepVelMag = list(float_range(6e-05, 10e-05, 1e-05))  # in km/s
# next we can have the pointing accurcy which is +/- 5 degrees in any direction which
# will effect the two angles that we defined for the orientation
pointingAccStart = -5 * (pi/180)
pointingAccStop = 5 * (pi/180)
pointingAccStep = 1 * (pi/180)
pointErrNormal = list(float_range(pointingAccStart, pointingAccStop, pointingAccStep))  # in rad
pointErrVel = list(float_range(pointingAccStart, pointingAccStop, pointingAccStep))     # in rad
# here we will create empty lists to hold our VNB values that will appended in for
# loops that will be written later.
sepVelRangeV = []
sepVelRangeN = []
sepVelRangeB = []
'''next we use these ranges to define the sep velocity vector and convert to VNB.
to do this we will create a for loop for each of the ranges described above and
nest them within each other.
do to the many nested loops the var that represents the place in the iteration were
written to be more descripted.'''
for iAngleFromNorm in range(len(angleFromNormalAxis)):
    for iAngleFromVel in range(len(angleFromVelAxis)):
        for iSepMag in range(len(sepVelMag)):
            for iPointErrNorm in range(len(pointErrNormal)):
                for iPointErrVel in range(len(pointErrVel)):
                    # here V, N and B are temp vars that will be appended on those empty
                    # lists that were created earlier.
                    V = sepVelMag[iSepMag] * sin(angleFromVelAxis[iAngleFromVel] + 
                        pointErrVel[iPointErrVel]) * cos(angleFromNormalAxis[iAngleFromNorm] + 
                        pointErrNormal[iPointErrNorm])
                    N = sepVelMag[iSepMag] * cos(angleFromVelAxis[iAngleFromVel] + 
                        pointErrVel[iPointErrVel])
                    B = sepVelMag[iSepMag] * sin(angleFromVelAxis[iAngleFromVel] + 
                        pointErrVel[iPointErrVel]) * sin(angleFromNormalAxis[iAngleFromNorm] + 
                        pointErrNormal[iPointErrNorm])
                    sepVelRangeV.append(V)
                    sepVelRangeN.append(N)
                    sepVelRangeB.append(B)

# here we will set the paths to save the GMAT reports and script files
# here I use an absolute path which makes the running of the scripts easier
pathScript = "C:/Users/mattg/Documents/GitHub/GMAT-automation/Generated-Scripts/"
pathReport = "C:/Users/mattg/Documents/GitHub/GMAT-automation/GMAT-Reports/"

# in order to write to the files the ranges need to be converted into strings
semiMajorAxisRange = list(map(str, semiMajorAxisRange))
eccentricityRange = list(map(str, eccentricityRange))
inclinationRange = list(map(str, inclinationRange))
sepVelRangeV = list(map(str, sepVelRangeV))
sepVelRangeN = list(map(str, sepVelRangeN))
sepVelRangeB = list(map(str, sepVelRangeB))

# now we will read in the template script into memory.
template = open("template.script", "r")

# now that all of our ranges have been set and the template file is loaded into memory
# we will create another set of nested for loops like for the separation vector
for iTime in range(len(timeRange)):
    for iDate in range(len(dateRange)):
        for iSMA in range(len(semiMajorAxisRange)):
            for iEcc in range(len(eccentricityRange)):
                for iInc in range(len(inclinationRange)):
                    for iSepVec in range(len(sepVelRangeV)):
                        # now these for loop will track and update our position in their
                        # given ranges, the first thing we need is a helpful filename
                        filename = (dateRange[iDate] + "_" + timeRange[iTime] + "_" + semiMajorAxisRange[iSMA] + "_"
                                    + eccentricityRange[iEcc] + "_" + inclinationRange[iInc] + "_"
                                    + sepVelRangeV[iSepVec] + "_" + sepVelRangeN[iSepVec] + "_"
                                    + sepVelRangeB[iSepVec])
                        # now we can use our new file name to create a file with that Name
                        currentFile = open(filename + ".script", 'w')
                        