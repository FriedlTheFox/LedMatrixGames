'''
Created on 22.10.2016

@author: Willi Meierhof
'''
import wx
from SerialInterface.SerialMatrixInterfaceDummy import SerialMatrixInterface,\
    InputApp
import random


class Color(object):
    RED = (255, 0, 0)
    YELLOW = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)


class Player(object):
    
    def __init__(self, color):
        self.color = color
        self.wins = 0
        self.enabled = False
        self.lastColumn = 4
        
    def GetColor(self):
        if self.enabled:
            return self.color
        else:
            return Color.BLACK
    
    def GetChipColor(self):
        return self.color

    def Disable(self):
        self.enabled = False
        
    def Enable(self):
        self.enabled = True
        
    def GetLastColumn(self):
        return self.lastColumn
    
    def SetColumn(self, column):
        self.lastColumn = column


class BorderSymbol(object):
    
    def __init__(self, color, solid=True):
        self.color = color
        self.solid = solid
        self.player = None
        
    def GetColor(self):
        if self.player is not None:
            return self.player.GetColor()
        return self.color
    
    def SetPlayer(self, player):
        if not self.solid:
            self.player = player
            
    def ResetBorder(self):
        self.player = None

class PlayField(object):
    
    def __init__(self):
        self.color = Color.BLACK
        self.setByPlayer = None
        
    def GetColor(self):
        if self.setByPlayer is not None:
            return self.setByPlayer.GetChipColor()
        else:
            return self.color
        
    def SetPlayer(self, player):
        self.setByPlayer = player

class PlayGround(object):
    def __init__(self, game):
        self.height = 7
        self.width = 7
        self.game = game
        
        self.fields = [[0 for x in range(self.width + 1)] for y in range(self.height + 1)]
        self.columns = [0, 0, 0, 0, 0, 0, 0]
    
    def GetField(self, *args):
        '''
        Get a Field by tupel "(x, y)" or "x, y"
        '''
        if isinstance(args[0], (tuple, list)):
            x, y = args[0]
        else:
            x = args[0]
            y = args[1]
        return self.fields[x][y]
    
    def Create(self):
        # Reset everything
        self.fields = [[0, 0, 0, 0, 0, 0, 0, 0],
                       [2, 1, 1, 1, 1, 1, 1, 1],
                       [2, 0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 0, 0, 0, 0, 0, 0]]
        
        for x in xrange(len(self.fields)):
            for y in xrange(len(self.fields[x])):
                if self.fields[x][y] == 1:
                    self.fields[x][y] = BorderSymbol(Color.BLUE, False)
                elif self.fields[x][y] == 2:
                    self.fields[x][y] = BorderSymbol(Color.BLUE)
                else:
                    self.fields[x][y] = PlayField()

    def SetPlayer(self, player, x, y):
        self.fields[x][y] = player

    def SetTopRowStone(self, activePlayer):
        column = activePlayer.GetLastColumn()
        self.fields[1][column].SetPlayer(activePlayer)

    def ResetTopRow(self):
        for index in xrange(7):
            self.fields[1][index+1].ResetBorder()
    
    def GetAmountOfColumn(self, column):
        return self.columns[column - 1]
    
    def AddStoneToColumn(self, column):
        if self.columns[column - 1] < 6:
            self.columns[column - 1] += 1
            return True
        else:
            return False        
    
    def SetStone(self, column, height, player):
        self.fields[8 -height][column].SetPlayer(player)
            
class ConnectFourGame(object):
    def __init__(self):
        self.SMI = SerialMatrixInterface(port='COM3',parent=None)
        self.inputApp = InputApp(self)
        self.playGround = PlayGround(self)
        self.playerRed = Player(Color.RED)
        self.playerYellow = Player(Color.YELLOW)
        self.activePlayer = None
        
    def DrawPlayGround(self):
        for y in xrange(self.playGround.height + 1):
            for x in xrange(self.playGround.width + 1):
                color = self.playGround.fields[y][x].GetColor()
                self.SMI.setPixel(x, y, color[0], color[1], color[2])    
    
    def CreatePlayGround(self):
        self.activePlayer = random.choice([self.playerRed, self.playerYellow])
        self.activePlayer.Enable()
        self.playGround.Create()
        self.playGround.SetPlayer(self.playerRed, 0, 0)
        self.playGround.SetPlayer(self.playerYellow, 0, 7)
        self.activePlayer.GetLastColumn()
        self.playGround.SetTopRowStone(self.activePlayer)
        self.DrawPlayGround()


    def switchPlayer(self):
        if self.playerRed is self.activePlayer:
            self.playerRed.Disable()
            self.playerYellow.Enable()
            self.activePlayer = self.playerYellow
        else:
            self.playerYellow.Disable()
            self.playerRed.Enable()
            self.activePlayer = self.playerRed
    
    def SetStone(self):
        columnToSet = self.activePlayer.GetLastColumn()
        if self.playGround.AddStoneToColumn(columnToSet):
            height = self.playGround.GetAmountOfColumn(columnToSet)
            self.playGround.SetStone(columnToSet, height, self.activePlayer)
            self.playGround.ResetTopRow()
            self.switchPlayer()           
            self.playGround.SetTopRowStone(self.activePlayer)
    
    def Move(self, direction):
        if direction == "DOWN":
            self.SetStone()
        else:
            newColumn = None
            if direction == "LEFT" and self.activePlayer.GetLastColumn() - 1 > 0:
                newColumn = self.activePlayer.GetLastColumn() - 1
            elif direction == "RIGHT" and self.activePlayer.GetLastColumn() + 1 < 8:
                newColumn = self.activePlayer.GetLastColumn() + 1
            if newColumn is not None:
                self.playGround.ResetTopRow()
                self.activePlayer.SetColumn(newColumn)
                self.playGround.SetTopRowStone(self.activePlayer)

        self.DrawPlayGround()
    
    def KeyHandler(self, evt):
        button = evt.GetEventObject()
        direction = button.GetLabel()
        self.Move(direction)
        evt.Skip()
        
if __name__ == '__main__':
    app = wx.App()
    game = ConnectFourGame()
    game.CreatePlayGround()
    app.MainLoop()
