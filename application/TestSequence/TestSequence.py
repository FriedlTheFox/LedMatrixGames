'''
Test sequence
'''

import time, random, sys, os
sys.path.append(os.path.join(os.getcwd(), "..\\..\\libraries"))
from SerialInterface import SerialMatrixInterface

class TestSequence():

    def __init__(self):
        self.SMI = SerialMatrixInterface.SerialMatrixInterface(port='COM3')

    def UpdateFullMatrix(self):
        while True:
            time.sleep(0.25)
            red   = random.randint(0, 255)
            green = random.randint(0, 255)
            blue  = random.randint(0, 255)
            print "Color is [%s, %s, %s]" % (red, green, blue)
            for x in xrange(8):
                for y in xrange(8):
                    self.SMI.setPixel(x, y, red, green, blue)

    def __del__(self):
        pass

if __name__ == "__main__":
    TS = TestSequence()
    TS.UpdateFullMatrix()