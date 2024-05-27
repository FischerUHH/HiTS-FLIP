
from ftdi_serial import Serial
from vicivalve import VICI

serial = Serial(device_serial='DT044VCL', baudrate=9600)
valve = VICI(serial=serial)


valve.home()
