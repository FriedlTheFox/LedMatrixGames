'''
Test sequence
'''

import time, random, sys, os, wx

sys.path.append(os.path.join(os.getcwd(), "..\\..\\libraries"))

from SerialInterface.SerialMatrixInterfaceDummy import InputApp
from SerialInterface import SerialMatrixInterfaceDummy
from SerialInterface import SerialMatrixInterface

class TestSequence(object):

    def __init__(self):
        try:
            self.SMI = SerialMatrixInterface.SerialMatrixInterface('COM3')
        except:
            self.SMI = SerialMatrixInterfaceDummy.SerialMatrixInterface('COM3', None, None)
        
        self.inputApp = InputApp(self)

    def UpdateFullMatrix(self):
        red   = random.randint(0, 255)
        green = random.randint(0, 255)
        blue  = random.randint(0, 255)
        #print "Color is [%s, %s, %s]" % (red, green, blue)
        for x in xrange(8):
            for y in xrange(8):
                self.SMI.setPixel(x, y, red, green, blue)

    def KeyHandler(self, evt):
        print evt.GetKeyCode()
        self.UpdateFullMatrix()
        evt.Skip()

    def __del__(self):
        pass

if __name__ == '__main__':
    app = wx.App()
    game = TestSequence()
    game.UpdateFullMatrix()
    app.MainLoop()