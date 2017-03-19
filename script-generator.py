# this program will be used to incremental change parameters from the template.script 
# file and save them to their own file. this will allow us to generate gmat script 
# files over the range of parameters that can be defined below.

# here we will define the range of dates and times to test the simulation over. 
dateRange = ['01 March 2016', '01 June 2016', '01 September 2016', '01 December 2016']
timeRange = ['00:00:00.000', '12:00:00.000']

# here we describe the range of state vector components for a keplarian state vector.
semiMajorAxisRange = range(6728.137, 6978.137, 50)  # kilometers
eccentricityRange = range(0.0, 0.9, 0.1)
inclinationRange = [28, 51.6]                       # inclination of ksc and ISS
