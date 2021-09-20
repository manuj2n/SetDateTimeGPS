#!/usr/bin/python3
# _*_ coding: utf8 _*_

from time import sleep
import serial

portwrite = "/dev/ttyUSB2"
port = "/dev/ttyUSB1"

def parseGPS(data):
    print(data, end='') #prints raw data
    if data[0:6] == "$GPRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            print("no satellite data available")
            return
        print("-----Parsing GPRMC-----")
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decode(sdata[3]) #latitude
        dirLat = sdata[4]      #latitude direction N/S
        lon = decode(sdata[5]) #longitute
        dirLon = sdata[6]      #longitude direction E/W
        speed = sdata[7]       #Speed in knots
        trCourse = sdata[8]    #True course
        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6] #date
        variation = sdata[10]  #variation
        sens = sdata[11]
        degreeChecksum = sdata[12]
        dc = degreeChecksum.split("*")
        degree = dc[0]        #degree
        checksum = dc[1]      #checksum

        latitude = lat.split()
        longitude = lon.split()
        print("time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, True Course : %s, Date : %s, Magnetic Variation : %s(%s),Checksum : %s "%    (time,lat,dirLat,lon,dirLon,speed,trCourse,date,variation,degree,checksum))


    else:
        print("Printed data is ",data[0:6])


def decode(coord):
    #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

print("Connecting port")
try:
    serw = serial.Serial(portwrite, baudrate = 115200, timeout = 1,rtscts=True, dsrdtr=True)
    serw.write('AT+QGPS=1\r')
    serw.close()
    sleep(1)
except Exception as e:
    print("Serial port failed")
    print(e)

print "Receiving GPS data"
ser = serial.Serial(port, baudrate = 115200, timeout = 0.5,rtscts=True, dsrdtr=True)
while True:
   data = ser.readline().decode('utf-8')
   parseGPS(data)
   sleep(1)