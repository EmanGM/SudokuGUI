import random


class SudokuAI:
    def __init__(self):

        self.board = [[0 for i in range(9)] for j in range(9)]
        self.SolutionBoard = self.board.copy() 
        self.row = 0
        self.column = 0
        self.backupRow = 0
        self.backupColum = 0
        self.genState = 0
        
    def setBoard(self, newBoard):
        self.board = newBoard.copy()
        self.SolutionBoard = self.board.copy() 


    def getNumber(self):
        return self.board[self.row][self.column]

    def findEmpty(self, descend=True):
        if descend:
            while True:
                self.column += 1
                if self.column > 8:
                    self.row += 1
                    if self.row > 8:
                        return False
                    else:
                        self.column = 0
                if self.toSolve[self.row][self.column] == 0:
                    return True
        else:
            self.column -= 1
            if self.column < 0:
                self.row -= 1
                if self.row < 0:
                    return False
                else:
                    self.column = 8
            while self.toSolve[self.row][self.column] != 0:
                self.column -= 1
                if self.column < 0:
                    self.row -= 1
                    if self.row < 0:
                        return False
                    else:
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

    def old_gen(self):

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
                    self.SolutionBoard = [i[:] for i in self.board]
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

    def gen(self):
        print("yes")
        for k in range(3):
            numbers = [n for n in range(1, 10)]
            for i in range(3*k, k*3 + 3):
                for j in range(i, i + 3):
                    number = random.choice(numbers)
                    while not self.isValid(number):
                        numbers.remove(numbers.index(number))
                        number = random.choice(numbers)
                    self.board[i][j] = number
                    return False
        return True

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
        rands = (random.randint(0, 8), random.randint(0, 8))
        if self.board[rands[0]][rands[1]] != 0:
            self.board[rands[0]][rands[1]] = 0
        else:
            self.removeCells()

    def clearAll(self):
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.SolutionBoard = self.board.copy()