# /*
#  * ----------------------------------------------------------------------------
#  * "THE BEER-WARE LICENSE" (Revision 42):
#  * Jeniffere@users.noreply.github.com wrote this file.  As long as you retain
#  * this notice you can do whatever you want with this stuff. If we meet some
#  * day, and you think this stuff is worth it, you can buy me a beer in return.
#  * Poul-Henning Kamp
#  * ----------------------------------------------------------------------------
#  */

from GameField import GameField
import time, sys, os, wx

sys.path.append(os.path.join(os.getcwd(), "..\\..\\libraries"))

from SerialInterface.SerialMatrixInterfaceDummy import TimeApp
from SerialInterface import SerialMatrixInterfaceDummy
from SerialInterface import SerialMatrixInterface

# Implementation of the game of life.
class GameOfLife(object):

    def __init__(self):
        self.initialState =[[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 0, 0, 0, 0],
                           [0, 0, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
        self.gameField = GameField(self.initialState)
        
        try:
            self.SMI = SerialMatrixInterface.SerialMatrixInterface('COM3')
        except:
            self.SMI = SerialMatrixInterfaceDummy.SerialMatrixInterface('COM3', None, None)

        self.inputApp = TimeApp(self)

    def DrawGameOfLife(self):
        self.gameField.calculateNextRound()
        x = 0
        y = 0
        currentField = self.gameField.getCurrentField()
        for line in currentField:
            for pixel in line:
                color = pixel * 255
                self.SMI.setPixel(x, y, 0, color, 0)
                x += 1
            y += 1
            x = 0

    def UpdateMatrix(self):
        time.sleep(0.5)
        self.DrawGameOfLife()

if __name__ == "__main__":
    app = wx.App()
    game = GameOfLife()
    #game.DrawGameOfLife()
    app.MainLoop()