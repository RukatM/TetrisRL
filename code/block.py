import pygame
import random
from settings import BLOCK_SPACE,BLOCK_COLORS,NEW_BLOCK_EVENT

class Block:
    def __init__(self,next_tetromino_letter = random.choice(list(BLOCK_COLORS.keys()))):
        self.tetrominoLetter = next_tetromino_letter
        self.tetrominoColor = BLOCK_COLORS[self.tetrominoLetter]
        self.tetrominoSpace = BLOCK_SPACE[self.tetrominoLetter][0]
        self.rotation = 0
        self.x = 5
        self.y = 0
        self.max_y = 20 - len(self.tetrominoSpace)
        self.max_x = 10 - len(self.tetrominoSpace[0])
    
    def generateBlock(self):
        print(self.tetrominoColor,self.tetrominoLetter,self.tetrominoSpace)
    
    def drawBlock(self,board):
        for i in range(len(self.tetrominoSpace)):
            for j in range(len(self.tetrominoSpace[i])):
                if self.tetrominoSpace[i][j] != 0:  
                    board.grid[i+self.y][j+self.x] =  self.tetrominoSpace[i][j]
                    board.gridColors[i+self.y][j+self.x] = self.tetrominoColor

    def moveRight(self,board):
        if self.checkRightCollision(board) == False:
            self.x += 1

    def moveLeft(self,board):
        if self.checkLeftCollision(board) == False:
            self.x -= 1

    def moveDown(self,board):
        if self.checkDownCollison(board) == False:
            self.y += 1
            
    def rotateR(self,board):
        
        if self.checkRotateCollison(board) == False:
            if self.rotation !=3:
                self.rotation += 1
            else:
                self.rotation = 0
        
        self.tetrominoSpace = BLOCK_SPACE[self.tetrominoLetter][self.rotation]
        self.max_y = 20 - len(self.tetrominoSpace)
        self.max_x = 10 - len(self.tetrominoSpace[0])

    def hardDrop(self,board):
        while self.checkDownCollison(board) == False:
            self.y += 1


    def checkDownCollison(self,board):
        if self.y == self.max_y:
            return True
        
        else:
            for i in range(len(self.tetrominoSpace[0])):
                if  board.grid[self.y + len(self.tetrominoSpace) ][self.x + i] == 1 and self.tetrominoSpace[-1][i] == 1:
                    return True 
            for i in range(len(self.tetrominoSpace) - 1, 0, -1):
                for j in range(len(self.tetrominoSpace[0])):
                    if self.tetrominoSpace[i][j] == 0 and board.grid[self.y+i][self.x+j] == 1 and self.tetrominoSpace[i-1][j] == 1:
                        return True
        return False
    
    def checkLeftCollision(self,board):
        if self.x != 0:
            for i in range(len(self.tetrominoSpace)):
                if self.tetrominoSpace[i][0] == 1 and board.grid[self.y + i][self.x-1] == 1:
                    return True
            return False
        else:
            return True
        
    def checkRightCollision(self,board):
        if self.x != self.max_x:
            for i in range(len(self.tetrominoSpace)):
                if self.tetrominoSpace[i][-1] == 1 and board.grid[self.y + i][self.x + len(self.tetrominoSpace[0])] == 1:
                    return True
            return False
        else:
            return True
        
    def checkNewBlockCollision(self,board):
        for i in range(len(self.tetrominoSpace)):
            for j in range(len(self.tetrominoSpace[i])):
                if self.tetrominoSpace[i][j] == 1 and board.grid[self.y + i][self.x + j] == 1:
                    return True
        return False
    
    def checkRotateCollison(self,board):
        if self.rotation !=3:
            next_rotation = self.rotation +1
        else:
            next_rotation = 0

        if len(BLOCK_SPACE[self.tetrominoLetter][next_rotation][0]) - len(self.tetrominoSpace[0]) + self.x > self.max_x:
            return True
        
        if len(BLOCK_SPACE[self.tetrominoLetter][next_rotation])> len(self.tetrominoSpace):
            if self.y + len(BLOCK_SPACE[self.tetrominoLetter][next_rotation]) <= self.max_y:
                for i in range(len(BLOCK_SPACE[self.tetrominoLetter][next_rotation][-1])):
                    if BLOCK_SPACE[self.tetrominoLetter][next_rotation][-1][i] == 1 and board.grid[self.y + len(BLOCK_SPACE[self.tetrominoLetter][next_rotation])][self.x +i] == 1:
                        return True
                
        elif len(BLOCK_SPACE[self.tetrominoLetter][next_rotation])< len(self.tetrominoSpace):
            if self.x + len(BLOCK_SPACE[self.tetrominoLetter][next_rotation][0]) <= self.max_x:
                for i in range(len(BLOCK_SPACE[self.tetrominoLetter][next_rotation])):
                    if BLOCK_SPACE[self.tetrominoLetter][next_rotation][i][-1] == 1 and  board.grid[self.y + i][self.x + len(BLOCK_SPACE[self.tetrominoLetter][next_rotation][0])] == 1:
                        return True
            

        
        return False
          
    
    

 

        
        
