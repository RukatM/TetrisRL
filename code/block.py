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
    
    def generateBlock(self):
        print(self.tetrominoColor,self.tetrominoLetter,self.tetrominoSpace)
    
    def drawBlock(self,board):
        
        for i in range(len(self.tetrominoSpace)):
            for j in range(len(self.tetrominoSpace[i])):
                board.grid[i+self.y][j+self.x] =  self.tetrominoSpace[i][j]

    def moveRight(self):
        if self.x < 9:
            self.x += 1

    def moveLeft(self):
        if self.x > 0:
            self.x -= 1

    def moveDown(self):
        if len(self.tetrominoSpace)  == 3:
            if self.y < 17:
                self.y += 1
            
        else:
            if self.y < 18:
                self.y += 1 
            

    def rotateR(self):
        if self.rotation !=3:
            self.rotation +=1
        else:
            self.rotation=0
        self.tetrominoSpace = BLOCK_SPACE[self.tetrominoLetter][self.rotation]
          
        

 

        
        
