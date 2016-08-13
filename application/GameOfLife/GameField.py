# /*
#  * ----------------------------------------------------------------------------
#  * "THE BEER-WARE LICENSE" (Revision 42):
#  * Jeniffere@users.noreply.github.com wrote this file.  As long as you retain
#  * this notice you can do whatever you want with this stuff. If we meet some
#  * day, and you think this stuff is worth it, you can buy me a beer in return.
#  * Poul-Henning Kamp
#  * ----------------------------------------------------------------------------
#  */

from Cell import Cell
import copy

class GameField():

    def __init__(self, initialState): 
        self.sizeX = len(initialState)
        self.sizeY = len(initialState[0])
        initialCells = [[Cell() for x in range(self.sizeY)] for y in range(self.sizeX)]
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                initialCells[i][j].setAlive(initialState[i][j])
        self.gameField = initialCells
        self.printField()
        
    def getCurrentField(self):
        currentValues = [[False for x in range(self.sizeY)] for y in range(self.sizeX)]
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                currentValues[i][j] = self.gameField[i][j].getAlive()
        return currentValues

    def printField(self):
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                print '{:4}'.format(self.gameField[i][j]),
            print
        print
        
    def countAliveNeighbours(self, idx, idy):
        count = 0
        for i in range(max(0,idx-1),min(idx+2,self.sizeX)):
            for j in range(max(0,idy-1),min(idy+2,self.sizeY)):
                if not (i == idx and j == idy):
                    if self.gameField[i][j].getAlive():
                        count += 1
        return count        
            
    def calculateNextRound(self):
        tmpGameField = [[Cell() for x in range(self.sizeY)] for y in range(self.sizeX)] 
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                neighbours = self.countAliveNeighbours(i,j)
                isAlive = self.gameField[i][j].isAliveInNextRound(neighbours)
                tmpGameField[i][j].setAlive(isAlive)
                
        self.gameField =  copy.deepcopy(tmpGameField)
        self.printField()
        