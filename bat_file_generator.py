'''
this script will load the files in our scripts directory into a list then
will write a .bat file to run these in GMAT. 
'''
# to find the filenames we will need to os module
from os import listdir

# for the path that the script files were saved to this will list the filenames in
# list that we will later loop through and write to a bat file.
pathScript = "C:/Users/mattg/Documents/GitHub/GMAT-automation/Generated-Scripts/"
scriptNames = listdir(pathScript)

# this var is the path to where your gmat.exe file is located
gmatPath = "C:/Program Files (x86)/GMAT/R2016a/bin"

# here we create the bat file
batFile = open('script_automation.bat', 'w')
# echo off just prevents the terminal from repeating the commands it is given
batFile.write("@ECHO OFF\n")
# now we change directory to be where our gmat.exe is
batFile.write("cd " + gmatPath + "\n")

# for a list of gmat commandline commands see...
# http://gmat.sourceforge.net/docs/R2012a/html/ch10s03.html#N1460B
# now that we are in the correct directory, we can loop through our script names list
# and write the commands to run gmat
for i in range(len(scriptNames)):
    batFile.write("GMAT.exe -r -x -m " + pathScript + scriptNames[i] + "\n")

