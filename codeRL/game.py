from settings import *
from menu import *
from board import Board
from block import Block
import random
import pygame

moveDown = False

class TetrisAI:
     def __init__(self):
         
          pygame.init()
          self.screen = pygame.display.set_mode((g_width + m_width + padding * 3,g_height + padding * 2))
          self.clock = pygame.time.Clock()
          pygame.display.set_caption("TetrisRL")
     
          self.game_space = pygame.Surface((g_width,g_height))
          self.menu_space = pygame.Surface((m_width,g_height))
          
          

          self.fall_speed = fall_speed
          self.timer_event = pygame.time.set_timer(MOVE_DOWN_EVENT, fall_speed)
          self.game_over = False
          self.next_block_letter = random.choice(list(BLOCK_COLORS.keys()))

          
          self.points = 0
          self.downDelay = 10
          self.reset()

          
          
     def reset(self):
          self.game_over = False
          self.board = Board(rows,collumns)
          self.block = Block()
          self.points = 0
          self.est_time = 0
          self.frame_iteration = 0
          self.reward = 0
   
     def playstep(self,action):
          self.frame_iteration += 1

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                         pygame.quit()
                         quit()

               elif event.type == MOVE_DOWN_EVENT:
                         self.move(2)

          
          
          self.move(action)

          
          
          if self.game_over:
               self.reward = -10
               return self.reward, self.game_over,self.points

          self.updateUI()
          self.checkCollision()


          pygame.display.update()
          self.clock.tick(60)
          return self.reward, self.game_over,self.points

     
     def move(self,action):
          if self.block.checkDownCollison(self.board):
               curr_points = self.points
               self.points += self.board.checkTetris()
               if self.points - curr_points > 0 and self.points - curr_points < 4000:
                    self.reward = 5
               elif self.points - curr_points == 4000:
                    self.reward =10
               self.newBlock()
               return
          
          if action == 0:
               self.block.moveLeft(self.board)
          elif action == 1:
               self.block.moveRight(self.board)
          elif action == 2:
               self.block.moveDown(self.board)
          elif action == 3:
               self.block.rotateR(self.board)
          elif action == 4:
               self.block.hardDrop(self.board)
          self.board.resetGrid()
          self.block.drawBlock(self.board)

          if self.block.checkDownCollison(self.board):
               curr_points = self.points
               self.points += self.board.checkTetris()
               if self.points - curr_points > 0 and self.points - curr_points < 4000:
                    self.reward = 5
               elif self.points - curr_points == 4000:
                    self.reward = 10
               self.newBlock()
          
     
     def updateUI(self):
          self.screen.fill((186, 0, 216))
          self.screen.blit(self.game_space, (10, 10))
          self.screen.blit(self.menu_space, (g_width + padding*2 , 10))
          
          #print(self.points)
          draw_text("NEXT", (g_width + padding*2 + m_width //2), 40,20,True,self.screen)
          draw_text("SCORE", (g_width + padding*2 + m_width //2), self.menu_space.get_height() //2-100,20,True,self.screen)
          draw_text(str(self.points), (g_width + padding*2 + m_width //2), self.menu_space.get_height() //2 -60,20,True,self.screen)
          self.board.drawNextBlock(self.screen,self.next_block_letter,(g_width + padding*2 + m_width //2)-60,80)

          self.game_space.fill((6,212,150))
          self.menu_space.fill((214,69,80))
          self.board.draw(self.game_space)

     def newBlock(self):
          self.board.updateTemplate()
          self.block = Block(self.next_block_letter)
          self.next_block_letter = random.choice(list(BLOCK_COLORS.keys()))
          print(self.next_block_letter)
          self.block.generateBlock()
          if self.block.checkNewBlockCollision(self.board):
               self.game_over = True
          else:
               self.block.drawBlock(self.board)

     def checkCollision(self):
          if self.block.checkDownCollison(self.board):
               if self.downDelay <0:
                    curr_points = self.points
                    self.points += self.board.checkTetris()
                    if self.points - curr_points > 0 and self.points - curr_points < 4000:
                         self.reward = 5
                    elif self.points - curr_points == 4000:
                         self.reward =10
                    self.newBlock()
                    self.downDelay = 10
               else:
                    self.downDelay -=1



