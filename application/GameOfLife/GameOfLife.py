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
import time, sys, os

sys.path.append(os.path.join(os.getcwd(), "..\\..\\libraries"))
from SerialInterface import SerialMatrixInterface

# Implementation of the game of life.
class GameOfLife():

    def main():  # @NoSelf
        initialState =[[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 1, 1, 0, 0, 0, 0],
                       [0, 0, 1, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 1, 0, 0],
                       [0, 0, 0, 0, 1, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]]
        gameField = GameField(initialState)
        SMI = SerialMatrixInterface.SerialMatrixInterface(port='COM3')
        while True:
            gameField.calculateNextRound()
            time.sleep(0.5)
            x = 0
            y = 0
            currentField = gameField.getCurrentField()
            for line in currentField:
                for pixel in line:
                    color = pixel * 50
                    SMI.setPixel(x, y, 0, color, 0)
                    x += 1
                y += 1
                x = 0

    if __name__ == "__main__":
        main()