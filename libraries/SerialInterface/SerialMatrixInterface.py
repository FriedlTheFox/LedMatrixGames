#!/usr/bin/env python
# -*- coding: utf-8 -*-

# /*
#  * ----------------------------------------------------------------------------
#  * "THE BEER-WARE LICENSE" (Revision 42):
#  * zwenson at rocketmail dot con wrote this file.  As long as you retain this notice you
#  * can do whatever you want with this stuff. If we meet some day, and you think
#  * this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
#  * ----------------------------------------------------------------------------
#  */

# Provide communication over serial port to MatrixDriver.

################ DEBUG #####################
try:
	from ipHelp import IPS, ip_syshook
	ip_syshook(1)

except ImportError:
	print 'ipHelp not available'
	pass
############################################



import serial
import numpy as np


class SerialMatrixInterface():

	NEWROW 	= np.int8(0xA0)
	ROWCOMPLETE = np.int8(0xB0)
	UP 		= np.int8(0xD0)
	DOWN 	= np.int8(0xD1)
	LEFT 	= np.int8(0xD2)
	RIGHT 	= np.int8(0xD3)

	READYTORECEIVE = np.int8(0x01)
	RECEIVEDROW = np.int8(0x02)

	def __init__(self, port = '/dev/ttyS4' , baud = '9600'):

		self.port = port
		self.baud = baud

		self.initSerialPort()

	def initSerialPort(self):

		self.ser = serial.Serial()
		self.ser.baudrate = self.baud
		self.ser.port = self.port

		try:
			self.ser.open()
		except:
			print 'Could not open serial port ' + self.port


	def move(self, direction, newRow):

		if direction not in ['left', 'right', 'up', 'down']:
			raise ValueError('Direction not implemented')
			return

		if newRow.shape != (3,8):
			raise ValueError('Wrong shape of row; Expected (3,8)')
			return

		ser.write(NEWROW)

		while(1):
			response = ser.readline()
			if response == READYTORECEIVE:
				break

		if direction == 'up':
			self.ser.write(UP)
		elif direction == 'down':
			self.ser.write(DOWN)
		elif direction == 'left':
			self.ser.write(LEFT)
		else:
			self.ser.write(RIGHT)

		for x in np.nditer(newRow):
			self.ser.write(x):

		self.ser.write(ROWCOMPLETE)

		i = 0
		while(i < 10):
			response = ser.readline()
			if response == RECEIVEDROW:
				return 0

			i +=1

		print 'Transmitting Row failed'
		return 1
		


	def __del__(self):
		self.ser.clos()




if __name__ == "__main__":


	SMI = SerialMatrixInterface()

	newRow = np.empty([3,8], dtype=np.int8)

	for x in np.nditer(newRow):
		print x

	IPS()

	SMI.move('up', newRow)

	IPS()
