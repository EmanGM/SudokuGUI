import pygame
import random
import sys

import SudokuAI

pygame.init()

size = width, height = 660, 600
x, y = 0, 1
#window can be a surface
window = pygame.display.set_mode(size)
offset = (60, 60)
clock = pygame.time.Clock()

class Cell:
    def __init__(self, position, Number):
        self.position = position
        self.rect = pygame.Rect(position, (50, 50))
        self.font = pygame.font.SysFont('Arial', 30, True) 
        self.number = Number
        self.color = (255, 255, 255)
        self.textSurface = self.font.render("{}".format(self.number), False, (0, 0, 0))
    
    def changeColor(self):
        self.color = (80, 80, 234)
        #self.textSurface = self.font.render("{}".format(self.number), False, self.color)

    def set_number(self, new_number):
        if new_number > 0:
            self.number = new_number
        self.color = (255, 255, 255)
        self.textSurface = self.font.render("{}".format(self.number), False, (0, 0, 0))

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect) 
        pygame.draw.rect(window, (0, 0, 0), self.rect, 2) 
        if self.number > 0:
            window.blit(self.textSurface, (self.position[0] + 10, self.position[1] + 10))

class Sudoku:

        
    def generateSudoku(self):
        if self.sudoku.gen():
            self.full = True
        self.setCells(self.sudoku.board)
   

    def solve(self):
        if not self.sudoku.solve():
            self.setCells(self.sudoku.board)
        else: 
            self.full = True

    def clear(self):
        
        self.sudoku.removeCells()
        self.setCells(self.sudoku.board)
        self.removeCellsNumber -= 1
        self.full = False
        if self.removeCellsNumber == 0:
            self.removeCellsNumber = 17
            return False      

        return True

    def clearAll(self):
        self.sudoku.clearAll()
        self.setCells(self.sudoku.board)


    def __init__(self):
        """
        Sudoku.TABLE = [[0, 0, 0, 2, 6, 0, 7, 0, 1], [6, 8, 0, 0, 7, 0, 0, 9, 0],[1, 9, 0, 0, 0, 4, 5, 0, 0],
                      [8, 2, 0, 1, 0, 0, 0, 4, 0], [0, 0, 4, 6, 0, 2, 9, 0, 0],[0, 5, 0, 0, 0, 3, 0, 2, 8],
                      [0, 0, 9, 3, 0, 0, 0, 7, 4], [0, 4, 0, 0, 5, 0, 0, 3, 6],[7, 0, 3, 0, 1, 8, 0, 0, 0]]
        """
        
        self.sudoku = SudokuAI.SudokuAI()
        self.setCells(self.sudoku.board)
        self.clock = pygame.time.Clock()
        self.timePoint = 0
        self.full = False
        self.editMode = False
        self.removeCellsNumber = 17


    def timer(self, time, fun):
        if pygame.time.get_ticks() / 1000 - self.timePoint > time:
            self.timePoint = pygame.time.get_ticks() / 1000
            return fun()
        else:
            return -1


    def colide_with(self, mousePos):
        self.mouseIndex = [(mousePos[x] - offset[x]) // 50, (mousePos[y] - offset[y]) // 50]
        for i in self.cells:
            if i.rect.collidepoint(mousePos):
                i.changeColor()

    def setNumber(self, number):
        print(self.mouseIndex)
        for cell in self.cells:
            if cell.color == (80, 80, 234):
                if self.editMode:
                    cell.set_number(number)
                    self.sudoku.board[self.mouseIndex[0]][self.mouseIndex[1]] = number
                    print(self.sudoku.board)
                else:
                    print("In solution", self.sudoku.SolutionBoard)
                    if self.sudoku.SolutionBoard[self.mouseIndex[y]][self.mouseIndex[x]] == number:
                        cell.set_number(number)
                        self.sudoku.SolutionBoard[self.mouseIndex[y]][self.mouseIndex[x]] = number
                    else:
                        cell.set_number(-1)

    def selecteBoard(self):
        self.editMode = not self.editMode


    def setCells(self, board):
        self.cells = [Cell((i*50 + offset[0], j*50 + offset[1]), board[j][i]) for i in range(9) for j in range(9)]

    def draw(self):
        for cell in self.cells:
            cell.draw()
        pygame.draw.line(window, (0, 0, 0), (3 * 50 + offset[x] - 1, offset[y]), (3 * 50 + offset[x] - 1, 9 * 50 + offset[y]), 6)
        pygame.draw.line(window, (0, 0, 0), (6 * 50 + offset[x] - 1, offset[y]), (6 * 50 + offset[x] - 1, 9 * 50 + offset[y]), 6)
        pygame.draw.line(window, (0, 0, 0), (offset[x], 3 * 50 + offset[y]), (9 * 50 + offset[x], 3 * 50 + offset[y]), 6)
        pygame.draw.line(window, (0, 0, 0), (offset[x], 6 * 50 + offset[y]), (9 * 50 + offset[x], 6 * 50 + offset[y]), 6)
        if self.editMode == True:
            outerEdge = pygame.Rect(offset[x], offset[y], 50*9, 50*9)
            pygame.draw.rect(window, (215, 30, 30), outerEdge, 6)


class Button:
    SIZE = [80, 20]

    def __init__(self, position, str):
        self.pos = position
        self.Rect = pygame.Rect((self.pos, Button.SIZE))
        self.font = pygame.font.SysFont('Arial', 12, True) 
        self.textSurface = self.font.render(str, False, (0, 0, 0))

    def checkClick(self, mousePos):
        if  self.Rect.collidepoint(mousePos):
            return True
        return False

    def draw(self):
        pygame.draw.rect(window, (160, 190, 160), self.Rect)
        window.blit(self.textSurface, (self.pos[0] + 5, self.pos[1] + 5))


def main():

    currentTime = 0

    sudoku = Sudoku()
    mouse = [0, 0]
    number = 0

    b5 = Button((550, 200), "Edit Board")
    b1 = Button((550, 240), "Gerar")
    b2 = Button((550, 280), "Eliminar Células")
    b3 = Button((550, 320), "Resolver")
    b4 = Button((550, 360), "Apagar tudo")

    actual_state = 0


    gameRunning = True
    while gameRunning:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    number = event.key - 48
                    print(number)
                    sudoku.setNumber(number)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse[0], mouse[1] = pygame.mouse.get_pos()
                    sudoku.colide_with(mouse)
                    if b1.checkClick(mouse):
                        print("V")
                        actual_state = "generate"
                    if b2.checkClick(mouse):
                        actual_state = "clear"
                    if b3.checkClick(mouse):
                        print("T")
                        actual_state = "solve"
                    if b4.checkClick(mouse):
                        print("Entrou")
                        sudoku.clearAll()
                        actual_state = ""
                    if b5.checkClick(mouse):
                        actual_state = "editModeAlert"
                        sudoku.selecteBoard()
            if event.type == pygame.QUIT:
                gameRunning = False 
    
        #print("Estado: ", actual_state)
        if actual_state == "generate" and not sudoku.full:
            sudoku.timer(0.01, sudoku.generateSudoku)
        elif actual_state == "solve" and not sudoku.full:
            sudoku.timer(0.1, sudoku.solve)
        elif actual_state == "clear":
            if not sudoku.timer(0.05, sudoku.clear):
                actual_state = ""
        elif actual_state == "editModeAlert":
            pass


        window.fill((210, 210, 210))
        sudoku.draw()
        b1.draw()
        b2.draw()
        b3.draw()
        b4.draw()
        b5.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()