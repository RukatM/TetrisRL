import pygame
from settings import tile_size,BLOCK_COLORS,BLOCK_SPACE


class Board:
    def __init__(self,rows,collumns):
        self.rows = rows
        self.collumns = collumns
        self.grid = [[0] * collumns for i in range(rows)]
        self.template = [[0] * collumns for i in range(rows)]
        self.gridColors = [[0] * collumns for i in range(rows)]
    
    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.collumns):
                pygame.draw.rect(screen, (0, 0, 0), (col * tile_size, row * tile_size, tile_size, tile_size), 1)
                if self.grid[row][col] != 0:
                    pygame.draw.rect(screen, self.gridColors[row][col],(col * tile_size, row * tile_size, tile_size, tile_size))
        
        for row in range(self.rows):
            for col in range(self.collumns):
                if self.grid[row][col] != 0:
                    pygame.draw.rect(screen, (0, 0, 0), (col * tile_size, row * tile_size, tile_size, tile_size), 1)
    
    def drawNextBlock(self,screen,key,x,y):
        space = BLOCK_SPACE[key]
        color = BLOCK_COLORS[key]
        if len(space[0][0]) == 3:
            x += 15
        elif len(space[0][0]) == 2:
            x+= 30

        for row in range(len(space[0])):
            for col in range(len(space[0][row])):
               
                if space[0][row][col] == 1:
                    tile_x = x + col * tile_size
                    tile_y = y + row * tile_size
                    pygame.draw.rect(screen, color, (tile_x, tile_y, tile_size, tile_size))
                    pygame.draw.rect(screen, (0, 0, 0), (tile_x, tile_y, tile_size, tile_size), 1)

    def resetGrid(self):
        for row in range(self.rows):
            for col in range(self.collumns):
                if self.grid[row][col] != self.template[row][col]:
                    self.grid[row][col] = self.template[row][col]
    
    def updateTemplate(self):
        for row in range(self.rows):
            for col in range(self.collumns):
                if self.grid[row][col] != self.template[row][col]:
                    self.template[row][col] = self.grid[row][col]
    
    def checkTetris(self):
        points_recieved = 0
        tetris_counter = 0
        i = len(self.grid) -1
        while i >= 0:
            if self.grid[i].count(1) == len(self.grid[0]):
                del self.grid[i]
                tetris_counter += 1
                del self.gridColors[i]
                self.grid.insert(0, [0] * self.collumns)
                self.gridColors.insert(0, [0] * self.collumns)
                i = len(self.grid) -1
            else:
                i -= 1
        bonus = 1
        for i in range(tetris_counter):
            points_recieved += bonus * 100
            bonus *= 3
        return points_recieved

   
        
                