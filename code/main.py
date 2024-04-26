from settings import *
from menu import *
from board import Board
from block import Block
import random
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
          self.game_over = False
          self.next_block_letter = random.choice(list(BLOCK_COLORS.keys()))

          self.est_time = 0
          
          self.points = 0
          


     def run(self):
          run = True
          while run:
               
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         run = False
                    elif event.type == pygame.KEYDOWN:

                         if event.key == pygame.K_LEFT:
                              self.block.moveLeft(self.board)
                              self.board.resetGrid()
                              self.block.drawBlock(self.board)   
                         
                         if event.key == pygame.K_RIGHT:
                              self.block.moveRight(self.board)
                              self.board.resetGrid()
                              self.block.drawBlock(self.board)

                         if event.key == pygame.K_DOWN:
                            
                              self.block.moveDown()
                              self.board.resetGrid()
                              self.block.drawBlock(self.board)

                         if event.key == pygame.K_c:
                              self.block.rotateR()
                              self.board.resetGrid()
                              self.block.drawBlock(self.board)
                         
                         if event.key == pygame.K_SPACE:
                              self.block.hardDrop(self.board)
                              self.board.resetGrid()
                              self.block.drawBlock(self.board)
                         
                         if event.key == pygame.K_r:
                              if self.game_over:
                                   self.game_over = False
                                   self.board = Board(rows,collumns)
                                   self.block = Block()
                                   self.points = 0




                    elif event.type == MOVE_DOWN_EVENT:
                         self.block.moveDown()
                         self.board.resetGrid()
                         self.block.drawBlock(self.board)
                         #print(self.block.y,self.block.x)
                         # print(self.block.y)

                    elif event.type == FALL_SPEED_EVENT:
                         self.fall_speed -= 100
                         self.timer_event = pygame.time.set_timer(MOVE_DOWN_EVENT, fall_speed)
                         # print(self.fall_speed)
                         
                    elif event.type == NEW_BLOCK_EVENT:
                         self.board.updateTemplate()
                         self.block = Block(self.next_block_letter)
                         self.next_block_letter = random.choice(list(BLOCK_COLORS.keys()))
                         print(self.next_block_letter)
                         self.block.generateBlock()
                         if self.block.checkNewBlockCollision(self.board):
                              self.game_over = True
                         else:
                              self.block.drawBlock(self.board)
                        
               
               

               self.screen.fill((186, 0, 216))
               self.screen.blit(self.game_space, (10, 10))
               self.screen.blit(self.menu_space, (g_width + padding*2 , 10))
               
               #print(self.points)
               draw_text("NEXT", (g_width + padding*2 + m_width //2), 40,20,True,self.screen)
               draw_text("POINTS", (g_width + padding*2 + m_width //2), self.menu_space.get_height() //2,20,True,self.screen)
               draw_text(str(self.points), (g_width + padding*2 + m_width //2), self.menu_space.get_height() //2 + 20,20,False,self.screen)
               self.board.drawNextBlock(self.screen,self.next_block_letter,(g_width + padding*2 + m_width //2)-60,80)
               
               if not self.game_over:
                    self.game_space.fill((5,189,134))
                    self.menu_space.fill((214,69,80))
                    self.board.draw(self.game_space)
                         
                    
                    if self.block.checkDownCollison(self.board):
                         self.points += self.board.checkTetris()
                         pygame.event.post(pygame.event.Event(NEW_BLOCK_EVENT))
               
               else:
                    draw_text("Game Over",self.screen.get_width() // 2, self.screen.get_height() // 2,40, True,self.screen)
                    draw_text("Press R to Restart",self.screen.get_width() // 2 , self.screen.get_height() // 2 + 100,30, True, self.screen)
                    

               pygame.display.update()
               self.est_time += self.clock.tick(60)
          pygame.quit()

main = Main()
main.run()