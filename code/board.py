import pygame
from settings import tile_size,g_height,g_width


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
        i = len(self.grid) -1
        while i >= 0:
            if self.grid[i].count(1) == len(self.grid[0]):
                del self.grid[i]
                del self.gridColors[i]
                self.grid.insert(0, [0] * self.collumns)
                self.gridColors.insert(0, [0] * self.collumns)
                i = len(self.grid) -1
            else:
                i -= 1
    def show_game_over_screen(self,screen):
        font = pygame.font.Font(None, 36)  
        text = font.render("Game Over", True, (255, 255, 255))  
        text_rect = text.get_rect(center=(g_width // 2, g_height // 2)) 
        screen.blit(text, text_rect) 

        pygame.display.flip()
    
        
                