#!/usr/bin/python3
'''
By this module the VICI valve can be acessed through the cpmmandline by typing
py setValve.py [pos]
whereas [pos] is a integer between 1 and 12.

Example: Set Valve to Position 5:
py setValve.py 5

All actions performed by this script are recorded in a directory on the Desktop in a .csv file for troubleshooting and later quality assessment.

Christian Ahlers
christian.ahlers@hotmail.de
0162/8424902
'''

# import all needes modules
from ftdi_serial import Serial
from vicivalve import VICI
from sys import argv
from getpass import getuser
from os import mkdir, path, popen
from time import strftime


#serial adress of valve
serialAdress = 'DT044VCL'

# string to write to file in case of an error 
re = ""

## set up connection to valve
# but first check if valve is connected
if serialAdress in Serial.list_device_serials():
    # define port by serial adress
    serial = Serial(device_serial=serialAdress, baudrate=9600)

    # define VICI class
    try:
        viciValve = VICI(serial=serial)
    except:
        re = "Error! Valve not connected or switched off."
else:
    re = "Error! Valve not connected or switched off."


# get position from commandline
pos = argv[-1]

## send command after quick sanity check
# if input from commandline is not a string of an integer number between 1 and 12
if pos not in [str(n) for n in list(range(1,13))]:
    # record error for log
    re = "".join(["Error! Wrong input. Command not send to valve via python. Input was:   ",pos])
    # check length of args
    if len(argv)<2:
        re = "Error! Please use this function from command line. for example type:           py setValve.py [pos]"
else:
    try:
        # send position to valve
        re = viciValve._send_and_receive("GO%i", pos)
    except:
        re = "".join(["Error. Valve was not responding. Returned: ",re])

## record action for QA
# check if we already have a dir for log
savedir ='C:\\MiSeq_Hits_Flip\\ViciVavleLogs\\' 
if not path.isdir(savedir):
    #if not, set one up
    mkdir(savedir)

# open file identifier (fid) with current date    
fid = open("".join([savedir,'ViciValveLogs',strftime("%y_%m_%d.txt")]),'a+')

# write date, time, the send position and the valves response
fid.write("\t".join([strftime("%d.%m.20%y\t%H:%M:%S"),pos,re,"\n"]))

#close fid
fid.close()

# alert user if error occurs
if "Error!" in re:
    print(re)
    popen("py C:\\MiSeq_Hits_Flip\\PythonCode\\sendErrorMessage.py "+ """ " """ +str(re)+""" " """)
    
    
           



