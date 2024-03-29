import pygame
from settings import tile_size


class Board:
    def __init__(self,rows,collumns):
        self.rows = rows
        self.collumns = collumns
        self.grid = [[0] * collumns for i in range(rows)]

    def draw(self,screen,block):
        for row in range(self.rows):
            for col in range(self.collumns):
                pygame.draw.rect(screen,(0,0,0),(col * tile_size,row * tile_size,tile_size,tile_size),1)
                if  self.grid[row][col] != 0:
                    pygame.draw.rect(screen,block.tetrominoColor,(col * tile_size,row * tile_size,tile_size,tile_size),20)
    def resetGrid(self,screen):
        for row in range(self.rows):
            for col in range(self.collumns):
                if self.grid[row][col] == 1:
                    self.grid[row][col] = 0
                    pygame.draw.rect(screen,(0,0,0),(col * tile_size,row * tile_size,tile_size,tile_size),1)
                
