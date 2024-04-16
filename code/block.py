import pygame
import random
import board
from settings import BLOCK_SPACE,BLOCK_COLORS

class Block:
    def __init__(self):
        self.tetrominoLetter = random.choice(list(BLOCK_COLORS.keys()))
        self.tetrominoColor = BLOCK_COLORS[self.tetrominoLetter]
        self.tetrominoSpace = BLOCK_SPACE[self.tetrominoLetter][0]
        self.rotation = 0
        self.x = 5
        self.y = 1
        self.max_y = 20 - len(self.tetrominoSpace)
        self.max_x = 10 - len(self.tetrominoSpace[0])
    
    def generateBlock(self):
        print(self.tetrominoColor,self.tetrominoLetter,self.tetrominoSpace)
    
    def drawBlock(self,board):
        
        for i in range(len(self.tetrominoSpace)):
            for j in range(len(self.tetrominoSpace[i])):
                board.grid[i+self.y][j+self.x] =  self.tetrominoSpace[i][j]

    def moveRight(self):
        if self.x < self.max_x:
            self.x += 1

    def moveLeft(self):
        if self.x > 0:
            self.x -= 1

    def moveDown(self):
        if self.y < self.max_y:
            self.y += 1
            

    def rotateR(self):
        if self.rotation !=3:
            self.rotation +=1
        else:
            self.rotation=0
        self.tetrominoSpace = BLOCK_SPACE[self.tetrominoLetter][self.rotation]
        self.max_y = 20 - len(self.tetrominoSpace)
        self.max_x = 10 - len(self.tetrominoSpace[0])
          
        

 

        
        
