'''this program will be used to incremental change parameters from the template.script
file and save them to their own file. this will allow us to generate gmat script
files over the range of parameters that can be defined below.'''

from math import sin, cos, pi

# here we will define the range of dates and times to test the simulation over.
dateRange = ['01 March 2016', '01 June 2016', '01 September 2016', '01 December 2016']
timeRange = ['00:00:00.000', '12:00:00.000']

def float_range(start, stop, step):
    '''python built in range() function doesn't work of floating point numbers.
    this is a simple function that loop saving your changing start value that will be
    incremented by your step value.
    note that to store the values in a list you have to use the list()
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
angleFromVelAxis = list(float_range(0, 2*pi, pi/3))           # in rad
# from here we set the variations of the velocity magnitude
sepVelMag = list(float_range(6e-05, 1e-04, 1e-05))  # in km/s
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
# next we use these ranges to define the sep velocity vector and convert to VNB
for iAngleFromNorm in range(len(angleFromNormalAxis)):
    for iAngleFromVel in range(len(angleFromVelAxis)):
        for iSepMag in range(len(sepVelMag)):
            for iPointErrNorm in range(len(pointErrNormal)):
                for iPointErrVel in range(len(pointErrVel)):
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
