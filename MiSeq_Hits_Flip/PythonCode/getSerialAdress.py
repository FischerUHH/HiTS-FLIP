from ftdi_serial import Serial
import time

print("The adresses of the devices connected to this PC are:")
for element in Serial.list_device_serials():
    print(" -   ",element)
time.sleep(1000)
