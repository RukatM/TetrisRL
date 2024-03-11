import pygame
import random
import board
from settings import BLOCK_SPACE,BLOCK_COLORS

class Block:
    def __init__(self):
        self.tetrominoLetter = random.choice(list(BLOCK_COLORS.keys()))
        self.tetrominoColor = BLOCK_COLORS[self.tetrominoLetter]
        self.tetrominoSpace = BLOCK_SPACE[self.tetrominoLetter]
    
    def generateBlock(self):
        print(self.tetrominoColor,self.tetrominoLetter,self.tetrominoSpace)
    
    def drawBlock(self,board):
        
        for i in range(len(self.tetrominoSpace)):
            for j in range(len(self.tetrominoSpace[i])):
                board.grid[i+1][j+5] =  self.tetrominoSpace[i][j]

    
        

        print(board.grid)
        print("rysuję")

        
        
