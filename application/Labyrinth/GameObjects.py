'''
Created on 28.08.2016

@author: Max
'''


class Player(object):
    def __init__(self, x=1, y=1):
        self.x = x
        self.y = y

    def SetPosition(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def GetPosition(self):
        return (self.x, self.y)

    def ResetPosition(self):
        self.x = 1
        self.y = 1

    def Move(self, direction):            
        if direction == "U":
            self.y -= 1
        elif direction == "D":
            self.y += 1
        elif direction == "L":
            self.x -= 1
        elif direction == "R":
            self.x += 1

class Field():
    def CanWalk(self):
        raise NotImplementedError

    def GetColor(self):
        raise NotImplementedError

    def Walk(self):
        pass


class Wall(Field):
    def CanWalk(self):
        return False

    def GetColor(self):
        return (0, 0, 150)


class Way(Field):
    def CanWalk(self):
        return True

    def GetColor(self):
        return (0, 0, 0)


class Door(Field):
    def __init__(self):
        self.locked = True

    def CanWalk(self):
        return not self.locked

    def GetColor(self):
        if self.locked:
            return (200, 0, 0)
        else:
            return (0, 200, 0)

    def Unlock(self):
        self.locked = False


class Key(Field):
    def __init__(self, door):
        self.door = door
        self.color = (255, 150, 0)

    def CanWalk(self):
        return True

    def GetColor(self):
        return self.color

    def Walk(self):
        self.color = (0, 0, 0)
        self.door.Unlock()
