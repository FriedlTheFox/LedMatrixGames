# /*
#  * ----------------------------------------------------------------------------
#  * "THE BEER-WARE LICENSE" (Revision 42):
#  * Jeniffere@users.noreply.github.com wrote this file.  As long as you retain
#  * this notice you can do whatever you want with this stuff. If we meet some
#  * day, and you think this stuff is worth it, you can buy me a beer in return.
#  * Poul-Henning Kamp
#  * ----------------------------------------------------------------------------
#  */

import unittest
from Cell import Cell
from GameField import GameField

class GameOfLifeTest(unittest.TestCase):

    def setUp(self):
        self.cell = Cell()
        
    def testDieBySolitude(self):
        self.cell.becomePopulated();
        self.assertEqual(self.cell.isAliveInNextRound(0), False)
        self.assertEqual(self.cell.isAliveInNextRound(1), False)

    def testDieByOverpopulation(self):
        self.cell.becomePopulated();
        self.assertEqual(self.cell.isAliveInNextRound(4), False)
        self.assertEqual(self.cell.isAliveInNextRound(5), False)
        self.assertEqual(self.cell.isAliveInNextRound(6), False)
        self.assertEqual(self.cell.isAliveInNextRound(7), False)
        self.assertEqual(self.cell.isAliveInNextRound(8), False)

    def testSurvive(self):
        self.cell.becomePopulated();
        self.assertEqual(self.cell.isAliveInNextRound(2), True)
        self.assertEqual(self.cell.isAliveInNextRound(3), True)

    def testBecomePopulated(self):
        self.cell.die();
        self.assertEqual(self.cell.isAliveInNextRound(3), True)

    def testRemainDead(self):
        self.cell.die();
        self.assertEqual(self.cell.isAliveInNextRound(0), False)
        self.assertEqual(self.cell.isAliveInNextRound(1), False)
        self.assertEqual(self.cell.isAliveInNextRound(2), False)
        self.assertEqual(self.cell.isAliveInNextRound(4), False)
        self.assertEqual(self.cell.isAliveInNextRound(5), False)
        self.assertEqual(self.cell.isAliveInNextRound(6), False)
        self.assertEqual(self.cell.isAliveInNextRound(7), False)
        self.assertEqual(self.cell.isAliveInNextRound(8), False)

    def testCount0Neighbours(self):
        initialState = [[False, False, False],
                        [False, False, False],
                        [False, False, False],
                        [False, False, False]]
        gameField = GameField(initialState)
        self.assertEqual(gameField.countAliveNeighbours(1,1), 0)

    def testCount8Neighbours(self):
        initialState = [[True, True, True],
                        [True, True, True],
                        [True, True, True],
                        [True, True, True]]
        gameField = GameField(initialState)
        self.assertEqual(gameField.countAliveNeighbours(1,1), 8)
        
    def testCountNeighbours(self):
        initialState =[[False,    False,    False],
                       [False,    True,     False],
                       [False,    True,     False],
                       [False,    True,     False],
                       [False,    False,    False]]
        gameField = GameField(initialState)
        self.assertEqual(gameField.countAliveNeighbours(3,1), 1)
        
    def testSimpleStaticObject(self):
        firstState =  [[False,    False,    False],
                       [False,    True,     False],
                       [True,     False,    True],
                       [False,    True,     False],
                       [False,    False,    False]]
         
        gameField = GameField(firstState)
        self.assertEqual(gameField.getCurrentField(), firstState)
        gameField.calculateNextRound()
        self.assertEqual(gameField.getCurrentField(), firstState)
        gameField.calculateNextRound()
        self.assertEqual(gameField.getCurrentField(), firstState)
    
    def testSimpleOscillatingObject(self):
        firstState =  [[False,    False,    False],
                       [False,    True,     False],
                       [False,    True,     False],
                       [False,    True,     False],
                       [False,    False,    False]]
         
        secondState = [[False,    False,    False],
                       [False,    False,    False],
                       [True,     True,     True],
                       [False,    False,    False],
                       [False,    False,    False]]
         
        gameField = GameField(firstState)
        self.assertEqual(gameField.getCurrentField(), firstState)
        gameField.calculateNextRound()
        self.assertEqual(gameField.getCurrentField(), secondState)
        gameField.calculateNextRound()
        self.assertEqual(gameField.getCurrentField(), firstState)
        gameField.calculateNextRound()
        self.assertEqual(gameField.getCurrentField(), secondState)       

if __name__ == '__main__':
    unittest.main()
