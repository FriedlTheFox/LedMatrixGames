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
from Cell import Cell

# Implementation of the game of life.
class GameOfLife():

    def main():  # @NoSelf
        size = 8
        initialState = [[Cell() for x in range(size)] for y in range(size)] 
        initialState[3][3].becomePopulated()
        initialState[3][4].becomePopulated()
        initialState[3][5].becomePopulated()
        gameField = GameField(initialState)
        gameField.calculateNextRound()
        gameField.calculateNextRound()

    if __name__ == "__main__":
        main()
            
