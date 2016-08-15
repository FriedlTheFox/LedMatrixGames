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
import time, serial

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
        ser = serial.Serial(port='COM3',
                            baudrate=115200,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS
                            )
        time.sleep(2)
        while True:
            gameField.calculateNextRound()
            time.sleep(0.05)
            x = 0
            y = 0
            currentField = gameField.getCurrentField()
            for line in currentField:
                for pixel in line:
                    color = pixel * 50
                    ser.write("%s,%s,0,%s,0\n" % (x,y,color))
                    #print "%s,%s,0,%s,0\n" % (x,y,color)
                    x += 1
                y += 1
                x = 0

    if __name__ == "__main__":
        main()
        ser.close()