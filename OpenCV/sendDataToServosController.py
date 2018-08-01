from time import sleep
import serial
import struct
import random


order = "132456".encode()
ser = serial.Serial('/dev/ttyUSB0', 9600)
print(ser.readline())


while True:
    s1 = random.randint(200, 800)
    s2 = random.randint(200, 800)
    s3 = random.randint(200, 800)
    s4 = random.randint(200, 800)
    s5 = random.randint(200, 800)
    s6 = random.randint(200, 800)

    a = struct.pack('<iiiiiiiiiBBBBBB', 0, 1000, 30, s1, s2, s3, s4, s5, s6,1,2,3,4,5,6)
    print(s1)
    print(s2)
    print(s3)
    print(s4)
    print(s5)
    print(s6)
    print(order)


    ser.write(a)

    print("Read data:")
    read = ser.readline()
    read1 = ser.readline()
    read2 = ser.readline()
    read3 = ser.readline()
    read4 = ser.readline()
    read5 = ser.readline()
    read6 = ser.readline()
    read7 = ser.readline()
    read8 = ser.readline()
    read9 = ser.read()


    for i in range(0,5):
        read9 = read9 + (ser.read())

    print(read)
    print(read1)
    print(read2)
    print(read3)
    print(read4)
    print(read5)
    print(read6)
    print(read7)
    print(read8)
    print(read9)

    ready = ser.readline()
    print(ready)

