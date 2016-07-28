'''
Moving DOT

created by Friedl the Fox
(c) 2015

'''

import time
import serial
import msvcrt

keyDict = {18656 : "up",
           19424 : "left",
           20704 : "down",
           19936 : "right",
           18912 : "pUp",
           20960 : "pDown",
           27    : "ESC",
           32    : "Space",
           43    : "+",
           45    : "-",
           114   : "r",
           103   : "g",
           98    : "b",
           107   : "k"}

def GetKey():
    if msvcrt.kbhit():
        a = ord(msvcrt.getch())
        if a == 0 or a == 224:
            b = ord(msvcrt.getch())
            x = a + (b*256)
            if x in keyDict.keys():
                return keyDict[x]
            else:
                print(x)
                return x
        else:
            if a in keyDict.keys():
                return keyDict[a]
            else:
                print(a)
                return a
    else:
        return None

def OpenSerial():
    return serial.Serial(
        port='COM3',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

def CheckSerial(ser):
    if ser.isOpen():
        ser.close()
        print 'close...'
        
    ser.open()
    if ser.isOpen():
        print 'open...'

    while ser.isOpen() == False:
        time.sleep(0.1)
        print 'wait...\n'

    time.sleep(2)

def CloseSerial(ser):
    ser.close()
    
def CubeSetPixelXY(ser, x, y, r, g, b, logInfo = True):
    ser.write(bytes('%s,%s,%s,%s,%s\n' % (x,y,r,g,b)))
    if logInfo:
        print '%s,%s,%s,%s,%s\n' % (x,y,r,g,b)
        
def CubeInit(ser):
    CubeReset(ser)
    CubeSetPixelXY(ser,7,0,255,0,0)

def CubeReset(ser):
    for x in range(8):
        for y in range(8):
            ser.write(bytes('%s,%s,0,0,0\n' % (x,y)))
    
def Main():
    ser = OpenSerial()
    CheckSerial(ser)
    CubeInit(ser)
    
    # init values
    x = 7
    y = 0
    r = 255
    g = 0
    b = 0
        
    key = ""
    color = "r"
    while key != "ESC":
        time.sleep(0.01)
        key = GetKey()
        if key in ["up", "down", "left", "right", "-", "+", "r", "g", "b"]:
            ser.write(bytes('%s,%s,0,0,0\n' % (x,y)))
            if key == "down" and x < 7:
                x += 1
            if key == "up" and x > 0:
                x -= 1
            if key == "right" and y < 7:
                y += 1
            if key == "left" and y > 0:
                y -= 1
            if key == "r":
                color = "r"
            if key == "g":
                color = "g"
            if key == "b":
                color = "b"
            if key == "+":
                if color == "r" and r < 255:
                    r += 5
                if color == "g" and g < 255:
                    g += 5
                if color == "b" and b < 255:
                    b += 5
            if key == "-":
                if color == "r" and r > 0:
                    r -= 5
                if color == "g" and g > 0:
                    g -= 5
                if color == "b" and b > 0:
                    b -= 5
            ser.write(bytes('%s,%s,%s,%s,%s\n' % (x,y,r,g,b)))
            print '%s,%s,%s,%s,%s' % (x,y,r,g,b)
        elif key in ["k"]:
            for x in range(8):
                for y in range(8):
                    ser.write(bytes('%s,%s,%s,%s,%s\n' % (x,y,0,50,100)))
        elif key in ["Space"]:
            CubeReset(ser)
    CloseSerial(ser)

Main()
