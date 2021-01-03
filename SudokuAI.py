import random


class SudokuAI:
    def __init__(self):
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.row = 0
        self.column = 0
        self.backupRow = 0
        self.backupColum = 0
        self.genState = 0


    def getNumber(self):
        return self.board[self.row][self.column]

    def findEmpty(self, descend=True):
        if descend:
            self.column += 1
            if self.column > 8:
                if self.row > 8:
                    return False
                else:
                    self.row += 1
                    self.column = 0
            while self.toSolve[self.row][self.column] != 0:
                self.column += 1
                if self.column > 8:
                    if self.row == 8:
                        return False
                    else:
                        self.row += 1
                        self.column = 0
        else:
            self.column -= 1
            if self.column < 0:
                if self.row < 0:
                    return False
                else:
                    self.row -= 1
                    self.column = 8
            while self.toSolve[self.row][self.column] != 0:
                self.column -= 1
                if self.column < 0:
                    if self.row < 0:
                        return False
                    else:
                        self.row -= 1
                        self.column = 8

        return True

    def isValid(self, number):
        #loop throught the row
        for i in range(9):
            if number == self.board[self.row][i]:
                return False

        #loop throught the colum
        for i in range(9):
            if number == self.board[i][self.column]:
                return False
        
        #loop throught the 3x3 square
        for i in range((self.row // 3) * 3, (self.row // 3) * 3 + 3):
            for j in range((self.column // 3) * 3, (self.column // 3) * 3 + 3):
                if number == self.board[i][j]:
                    return False
        
        return True

    def gen(self):

        if self.genState == 0:
            number = self.getNumber()
            while not self.isValid(number):
                number += 1
                if number > 9:
                    self.board[self.row][self.column] = 0
                    self.backupRow = self.row
                    self.backupColum = self.column
                    self.genState = 1
                    return False
            self.board[self.row][self.column] = number
            self.column += 1
            if self.column > 8:
                if self.row == 8:
                    return True
                else:
                    self.row += 1
                    self.column = 0

        elif self.genState == 1:
            self.column -= 1
            if self.column < 0:
                self.row -= 1
                self.column = 8
            number = self.getNumber()
            while not self.isValid(number):
                number += 1
                if number > 9:
                    self.board[self.row][self.column] = 0
                    self.backupRow = self.row
                    self.backupColum = self.column
                    return False
            self.board[self.row][self.column] = number
            self.row = self.backupRow
            self.column = self.backupColum
            self.genState = 0

    def solve(self):

        if self.genState == 0:
            self.toSolve = [i[:] for i in self.board]
            self.row = 0
            self.column = -1
            self.genState = 1

        elif self.genState == 1:
            if not self.findEmpty(True): 
                return True
            else:
                number = self.getNumber()
                while not self.isValid(number):
                    number += 1
                    if number > 9:
                        self.board[self.row][self.column] = 0
                        self.genState = 2
                        return False
                self.board[self.row][self.column] = number

        elif self.genState == 2:
            if not self.findEmpty(False): 
                return True
            else:
                number = self.getNumber()
                while not self.isValid(number):
                    number += 1
                    if number > 9:
                        self.board[self.row][self.column] = 0
                        return False
                self.board[self.row][self.column] = number
                self.genState = 1

    def removeCells(self):
        self.board[random.randint(0, 8)][random.randint(0, 8)] = 0