from settings import *
from menu import *
from board import Board
from block import Block
import random
import pygame

moveDown = False

class Main:
     def __init__(self):
         
          pygame.init()
          self.screen = pygame.display.set_mode((g_width + m_width + padding * 3,g_height + padding * 2))
          self.clock = pygame.time.Clock()
          pygame.display.set_caption("TetrisRL")
     
          self.game_space = pygame.Surface((g_width,g_height))
          self.menu_space = pygame.Surface((m_width,g_height))
          
          self.reset()

          self.fall_speed = fall_speed
          self.timer_event = pygame.time.set_timer(MOVE_DOWN_EVENT, fall_speed)
          self.game_over = False
          self.next_block_letter = random.choice(list(BLOCK_COLORS.keys()))

          
          self.points = 0

          self.moveDown = False
          self.moveLeft = False
          self.moveRight = False
          self.hardDrop = False
          self.rotateR = False

          self.moveDelay = 3
          self.downDelay = 10

          
          
     def reset(self):
          self.game_over = False
          self.board = Board(rows,collumns)
          self.block = Block()
          self.points = 0
          self.est_time = 0
          self.frame_iteration = 0
   
     def playstep(self):
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                         pygame.quit()
                         quit()
               elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                         self.moveLeft = True
                    elif event.key == pygame.K_RIGHT:
                         self.moveRight = True
                    elif event.key == pygame.K_DOWN:
                         self.moveDown = True
                    elif event.key == pygame.K_c:
                         self.rotateR = True
                    elif event.key == pygame.K_SPACE:
                         self.hardDrop = True
               
               elif event.type == MOVE_DOWN_EVENT:
                         self.move(2)
        
          if self.moveLeft:
               self.move(0)
               self.moveLeft=False
          if self.moveRight:
               self.move(1)
               self.moveRight=False
          if self.moveDown:
               self.move(2)
               self.moveDown= False
          if self.rotateR:
               self.move(3)
               self.rotateR = False
          if self.hardDrop:
               self.move(4)
               self.hardDrop = False
          if self.game_over:
               self.reset()
          
          self.updateUI()
          self.checkCollision()


          pygame.display.update()
          self.clock.tick(60)

     
     def move(self,action):
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
                    self.points += self.board.checkTetris()
                    self.newBlock()
                    self.downDelay = 10
               else:
                    self.downDelay -=1


     def run(self):

          while True:
               self.playstep()

main = Main()
main.run()