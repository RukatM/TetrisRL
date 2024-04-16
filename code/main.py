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
         # pygame.display.set_icon(icon)
     
          self.game_space = pygame.Surface((g_width,g_height))
          self.menu_space = pygame.Surface((m_width,g_height))
          
          self.board = Board(rows,collumns)

          self.block = Block()

          self.fall_speed = fall_speed
          self.timer_event = pygame.time.set_timer(MOVE_DOWN_EVENT, fall_speed)
          self.timer_event = pygame.time.set_timer(FALL_SPEED_EVENT, 10000)

          self.est_time = 0
          
          


     def run(self):
          run = True
          while run:
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         run = False
                    elif event.type == pygame.KEYDOWN:

                         if event.key == pygame.K_LEFT:
                              self.block.moveLeft()
                              self.board.resetGrid()
                              self.block.drawBlock(self.board)   
                         
                         if event.key == pygame.K_RIGHT:
                              self.block.moveRight()
                              self.board.resetGrid()
                              self.block.drawBlock(self.board)
                              # print(self.block.x)

                         if event.key == pygame.K_DOWN:
                            
                              self.block.moveDown()
                              self.board.resetGrid()
                              self.block.drawBlock(self.board)

                         if event.key == pygame.K_SPACE:
                              self.block.rotateR()
                              self.board.resetGrid()
                              self.block.drawBlock(self.board)

                    elif event.type == MOVE_DOWN_EVENT:
                         self.block.moveDown()
                         self.board.resetGrid()
                         self.block.drawBlock(self.board)
                         print(self.block.y,self.block.x)
                         # print(self.block.y)

                    elif event.type == FALL_SPEED_EVENT:
                         self.fall_speed -= 100
                         self.timer_event = pygame.time.set_timer(MOVE_DOWN_EVENT, fall_speed)
                         # print(self.fall_speed)
                         
                    elif event.type == NEW_BLOCK_EVENT:
                         self.board.updateTemplate()
                         self.block = Block()
                         self.block.generateBlock()
                         self.block.drawBlock(self.board)
               
                         
                         


                         

               
               self.screen.fill((186, 0, 216))
               self.screen.blit(self.game_space, (10, 10))
               self.screen.blit(self.menu_space, (g_width + padding*2 , 10))
               
               self.game_space.fill((211, 126, 183))
               self.menu_space.fill((90, 0, 185))
               
               self.board.draw(self.game_space,self.block)
                    
               
               if self.block.checkCollison(self.board):
                    pygame.event.post(pygame.event.Event(NEW_BLOCK_EVENT))
                    
               pygame.display.update()
               self.est_time += self.clock.tick(60)


          pygame.quit()

main = Main()
main.run()