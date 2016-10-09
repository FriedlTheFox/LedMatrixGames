'''
Created on 28.08.2016

@author: Max
'''
import sys
import os

sys.path.append(os.path.join(os.getcwd(), "..\\..\\libraries"))

import wx
import random
import time

from SerialInterface.SerialMatrixInterfaceDummy import InputApp
from SerialInterface import SerialMatrixInterfaceDummy

from GameObjects import Wall, Way, Door, Key, Player
from SegmentMatrix import getMatrix


class Labyrinth(object):
    def __init__(self, game):
        self.height = 7
        self.width = 7
        self.game = game

        self.fields = []

    def GetField(self, *args):
        # Get a Field by tupel "(x, y)" or "x, y"
        if isinstance(args[0], (tuple, list)):
            x, y = args[0]
        else:
            x = args[0]
            y = args[1]
        return self.fields[x][y]

    def Create(self):
        # for increasing labyrinth size with level
        # comment out for constant size (given in init)
        self.height = self.game.level * 2 + 7
        self.width = self.game.level * 2 + 7

        # Reset everything to walls first
        self.fields = [[Wall() for _ in range(self.height)] for _ in range(self.width)]

        # first cell
        currentCell = (1, 1)

        # Create a stack for all cells to look at and remember all visited cells
        stack = []
        visitedCells = [currentCell]

        # Calculate how many cells must be visited
        maxLen = ((self.height) / 2) * ((self.width) / 2)

        # door and key positions, asign later
        doorPos = False
        keyPos = False

        # As long as there are cells that have not been visited
        while len(visitedCells) < maxLen:
            # Make the current cell a way
            col = currentCell[0]
            row = currentCell[1]
            self.fields[col][row] = Way()

            # Get all neighbours of the current cell that have not been visited
            neighbours = []
            if (self.width - 2 > col) and (col + 2, row) not in visitedCells:
                neighbours.append((col + 2, row))
            if (1 < col) and (col - 2, row) not in visitedCells:
                neighbours.append((col - 2, row))
            if (self.height - 2 > row) and (col, row + 2) not in visitedCells:
                neighbours.append((col, row + 2))
            if (1 < row) and (col, row - 2) not in visitedCells:
                neighbours.append((col, row - 2))

            # If there are any unvisited neighbours choose one, make it the current cell,
            # make it a way, append to the stack and mark as visited
            if neighbours:
                currentCell = random.choice(neighbours)
                # Make the field between the current Cell and the chosen neighbour a Way
                self.fields[(currentCell[0] + col) / 2][(currentCell[1] + row) / 2] = Way()

                stack.append(currentCell)
                visitedCells.append(currentCell)

            # If there are no unvisited neighbours get the next cell from the stack
            # and make it the current cell
            elif stack:
                currentCell = stack.pop()

                # At end of first corridor add the door
                if not doorPos:
                    doorPos = (col, row)

                # Add the key for the door and also make sure that this is not the door.
                # This can happen in small levels and fucks it all up.
                elif not keyPos and doorPos != (col, row) and random.randint(0, 10) > 5:
                    keyPos = (col, row)

        self.fields[currentCell[0]][currentCell[1]] = Way()

        # In very small labyrinths it's possible that no Key/Door pair was created.
        if doorPos is False or keyPos is False:
            # Just do it again until it works :)
            self.Create()
        else:
            # Create the Door at the given position
            door = self.fields[doorPos[0]][doorPos[1]] = Door()
            # Walking into unlocked Door = next level
            door.Walk = lambda: self.game.EndLabyrinth()
            # Create the actual Key for the Door
            self.fields[keyPos[0]][keyPos[1]] = Key(door)
    
            # Unfreeze game, so keyboard input is accepted again
            self.game.freeze = False

    def _debugOutput(self):
        for x in range(self.width):
            for y in range(self.height):
                color = self.fields[x][y].GetColor()
                self.game.SMI.setPixel(x, y, color[0], color[1], color[2])


class LabyrinthGame(object):
    def __init__(self):
        self.SMI = SerialMatrixInterfaceDummy.SerialMatrixInterface('COM3', None, None)
        
        self.inputApp = InputApp(self)
        self.lab = Labyrinth(self)

        self.player = Player()

        self.level = 0
        self.freeze = False

    def DrawLabyrinth(self):
        col, row = self.player.GetPosition()
        for x in range(-3, 5):
            for y in range(-3, 5):
                if 0 <= (x + col) < self.lab.width and 0 <= (y + row) < self.lab.height:
                    # Get color of field (wall, way, key, door)
                    color = self.lab.fields[x + col][y + row].GetColor()
                else:
                    # If outside of map
                    color = (0, 0, 0)
                self.SMI.setPixel(7 - (x + 3), y + 3, color[0], color[1], color[2])

        # Player
        self.SMI.setPixel(4, 3, 255, 255, 255)

    def CreateLabyrinth(self):
        self.player.ResetPosition()
        self.lab.Create()
        self.DrawLabyrinth()

    def DrawLevelNumber(self):
        levelString = "%03d" % (self.level)

        for shift in range(-8, 12, 1):
            for row in range(1, 6):
                for col in [shift + 4, shift, shift - 4]:
                    if 0 <= col < 8:
                        self.SMI.setPixel(col, row, 0, 0, 100)


            for n, ch in enumerate(levelString):
                mtx = getMatrix(ch)
    
                for col in range(3):
                    for row in range(5):
                        x = (7 - (col + (n * 4)) + shift)
                        if 8 > x >= 0:
                            if mtx[col][row] == 1:
                                self.SMI.setPixel(x, row + 1, 255, 0, 0)
                            else:
                                self.SMI.setPixel(x, row + 1, 0, 0, 100)
            time.sleep(0.2)

        self.CreateLabyrinth()

    def EndLabyrinth(self):
        # threading-Timer stuff is done, so the input wxApp (and the dummy if used)
        # doesnt freeze and can be closed, but keyboard input is disabled with self.freeze
        # TODO: better solution

        self.freeze = True
        self.level += 1

        from threading import Timer
        time = 0.1
        for row in range(8):
            for col in range(8):
                Timer(time, self.SMI.setPixel, [col, row, 0, 0, 100]).start()
                time += 0.02

        Timer(2, self.DrawLevelNumber).start()

    def Move(self, direction):
        col, row = self.player.GetPosition()
        if (direction is not None and not self.freeze and
            ((direction == "U" and self.lab.GetField(col, row - 1).CanWalk()) or
            (direction == "D" and self.lab.GetField(col, row + 1).CanWalk()) or
            (direction == "L" and self.lab.GetField(col - 1, row).CanWalk()) or
            (direction == "R" and self.lab.GetField(col + 1, row).CanWalk()))):
                self.player.Move(direction)

                self.lab.GetField(self.player.GetPosition()).Walk()
                self.DrawLabyrinth()

    def KeyHandler(self, evt):
        if evt.GetKeyCode() == 87:
            direction = "U"
        elif evt.GetKeyCode() == 65:
            direction = "L"
        elif evt.GetKeyCode() == 83:
            direction = "D"
        elif evt.GetKeyCode() == 68:
            direction = "R"
        else:
            direction = None

        self.Move(direction)
        evt.Skip()

if __name__ == '__main__':
    app = wx.App()
    game = LabyrinthGame()
    game.CreateLabyrinth()
    app.MainLoop()
