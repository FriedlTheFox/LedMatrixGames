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
import time

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
        while True:
            gameField.calculateNextRound()
            time.sleep(1)

    if __name__ == "__main__":
        main()
            
