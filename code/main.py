from settings import *
from board import Board
from block import Block
import pygame

class Main:
     def __init__(self):
         
          pygame.init()
          self.screen = pygame.display.set_mode((g_width + m_width + padding * 3,g_height + padding * 2))
          self.clock = pygame.time.Clock()
          pygame.display.set_caption("TetrisRL")
          pygame.display.set_icon(icon)
     
          self.game_space = pygame.Surface((g_width,g_height))
          self.menu_space = pygame.Surface((m_width,g_height))
          
          self.board = Board(rows,collumns)
          self.block = None

          self.elapsed_time = 0
          


     def run(self):
          run = True
          while run:
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         run = False

               
               self.screen.fill((186, 0, 216))
               self.screen.blit(self.game_space, (10, 10))
               self.screen.blit(self.menu_space, (g_width + padding*2 , 10))
               
               self.game_space.fill((211, 126, 183))
               self.menu_space.fill((90, 0, 185))
               
               self.board.draw(self.game_space,self.block)
               
               
               if self.block is None or self.elapsed_time >= 10000:
                    self.board.resetGrid(self.screen)
                    self.elapsed_time = 0
                    self.block = Block()
                    self.block.generateBlock()
                    self.block.drawBlock(self.board)
                    
                    
               
               pygame.display.update()
               self.elapsed_time += self.clock.tick(60)


          pygame.quit()

main = Main()
main.run()