'''
serial dummy
'''

import time
import serial
import random

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
   
def UpdateBuffer(ser, x, y, r, g, b, logInfo = True):
    ser.write('%s,%s,%s,%s,%s\n' % (x,y,r,g,b))
    if logInfo:
        print '%s,%s,%s,%s,%s\n' % (x,y,r,g,b)
        
def CubeInit(ser):
    CubeReset(ser)
    
def CubeReset(ser):
    ser.write('0,0,0\n')
    
def Main():
    ser = OpenSerial()
    CheckSerial(ser)
    CubeInit(ser)

    while True:
        ser.write('1,1,255,255,255\n')
        #ser.write('%s,%s,%s,%s,%s\n' % (random.randint(0,7), random.randint(0,7), random.randint(0,150), random.randint(0,150), random.randint(0,150)))
        time.sleep(1)

    CloseSerial(ser)
        

Main()
