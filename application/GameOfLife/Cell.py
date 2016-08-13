# /*
#  * ----------------------------------------------------------------------------
#  * "THE BEER-WARE LICENSE" (Revision 42):
#  * Jeniffere@users.noreply.github.com wrote this file.  As long as you retain
#  * this notice you can do whatever you want with this stuff. If we meet some
#  * day, and you think this stuff is worth it, you can buy me a beer in return.
#  * Poul-Henning Kamp
#  * ----------------------------------------------------------------------------
#  */

class Cell():

    def __init__(self):
        self.isAlive = False
    
    def getAlive(self):
        return self.isAlive
    
    def setAlive(self, isAlive):
        self.isAlive = isAlive
    
    def die(self):
        self.isAlive = False
    
    def becomePopulated(self):
        self.isAlive = True

    def isAliveInNextRound(self, aliveNeighbours):
        if not self.isAlive:
            if aliveNeighbours == 3:
                return True
        else:
            if aliveNeighbours < 2:
                return False
            elif aliveNeighbours > 3:
                return False
            
        return self.isAlive

    def __str__(self):
        return str(int(self.isAlive))

    
            
