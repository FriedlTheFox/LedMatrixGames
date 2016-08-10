'''
serial dummy
'''

import time
import serial

def OpenSerial():
    return serial.Serial(
        port='COM3',
        baudrate=9600,
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
   
def UpdateBuffer(ser, r, g, b, logInfo = True):
    ser.write(bytes('%s,%s,%s\n' % (r,g,b)))
    if logInfo:
        print '%s,%s,%s\n' % (r,g,b)
        
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

    UpdateBuffer(0xFF,0x00,0x00)

    CloseSerial(ser)
        

Main()
