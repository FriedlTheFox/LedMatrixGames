#!/usr/bin/env python
# -*- coding: utf-8 -*-

# /*
#  * ----------------------------------------------------------------------------
#  * "THE BEER-WARE LICENSE" (Revision 42):
#  * zwenson at rocketmail dot com wrote this file.  As long as you retain this notice you
#  * can do whatever you want with this stuff. If we meet some day, and you think
#  * this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
#  * ----------------------------------------------------------------------------
#  */

# Generate mazes using different algorithmś https://en.wikipedia.org/wiki/Maze_generation_algorithm
# Also provide functionality to move through the maze

################ DEBUG #####################
try:
	from ipHelp import IPS, ip_syshook
	ip_syshook(1)

except ImportError:
	print 'ipHelp not available'
	pass
############################################


import numpy as np


MOVEUP 		= np.array([0,1])
MOVEDOWN 	= np.array([0,-1])
MOVERIGHT 	= np.array([1,0])
MOVELEFT 	= np.array([-1,0])

BLACK = np.array([0,0,0], dtype=np.int8)
WHITE = np.array([255,255,255], dtype=np.int8)


class Maze():


	def __init__(self, algorithm = 'recursive backtracker' , dimension = [8,8]):

		self.pos = np.array([0,0])
		self.dimension = dimension
		self.generateMaze(algorithm)
		


	def move(self, direction): #up, down, left, right



		if direction == 'up':
			newPos = self.pos + MOVEUP
			if (self.field[:,newPos[0],newPos[1]] == BLACK).all():
				self.pos+=MOVEUP
				return 'pass'
			else:
				return 'wall'

		#elif 

		#else:
			#print 'Unknown direction' 
			#return 'wall'

		#return 'wall', 'pass', 'exit', ...


	def generateMaze(self, algorithm):

		if algorithm == 'recursive backtracker':
			self.generateMazeRecursiveBacktracker()

	def generateMazeRecursiveBacktracker(self):

		self.field = np.zeros([3] + self.dimension, dtype=np.int8)

		self.field[1,0,1] = 1

		


if __name__ == "__main__":


	M = Maze()

	M.move('up')

	IPS()