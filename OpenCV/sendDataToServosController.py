from time import sleep
import serial
import struct
import random


ser = serial.Serial()#('/dev/ttyUSB0', 9600)
ser.port = '/dev/ttyUSB0'
ser.baudrate = 9600
ser.setDTR(True)
ser.setRTS(True)
ser.open()
print(ser.readline())

while True:



    s1 = random.randint(200, 800)
    s2 = random.randint(200, 800)
    s3 = random.randint(200, 800)
    s4 = random.randint(200, 800)
    s5 = random.randint(200, 800)
    s6 = random.randint(200, 800)

    a = struct.pack('<iiiiiiiiiBBBBBB', 0, 1000, 30, s1, s2, s3, s4, s5, s6,1,2,3,4,5,6)

    ser.write(a)

    print("Read data:")
    ready = ser.readline()
    print(ready)



