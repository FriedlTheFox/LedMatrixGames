#!/usr/bin/env python
# -*- coding: utf-8 -*-

# /*
#  * ----------------------------------------------------------------------------
#  * "THE BEER-WARE LICENSE" (Revision 42):
#  * zwen@posteo.de wrote this file.  As long as you retain this notice you
#  * can do whatever you want with this stuff. If we meet some day, and you think
#  * this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
#  * ----------------------------------------------------------------------------
#  */

# Generate mazes using different algorithmś https://en.wikipedia.org/wiki/Maze_generation_algorithm
# Also provide functionality to move through the maze

import numpy as np


class Maze():

	MOVEUP 		= np.array([0,1])
	MOVEDOWN 	= np.array([0,-1])
	MOVERIGHT 	= np.array([1,0])
	MOVELEFT 	= np.array([-1,0])

	def __init__(self, algorithm = 'recursive backtracker' , dimension = [8,8]):

		self.pos = (0,0)
		self.dimension = dimension
		self.generate_maze(algorithm)
		

	def move(self, direction): #up, down, left, right


		if direction == 'up':
			if self.field(tuple(self.pos + MOVEUP)) == ' ':
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

		self.field = np.chararray(self.dimension)
		self.field[:] = '#'

