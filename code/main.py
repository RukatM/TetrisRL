from settings import *
import pygame

class Main:
     def __init__(self):
         
          pygame.init()
          self.screen = pygame.display.set_mode((g_width + m_width,g_height + m_height))
          self.clock = pygame.time.Clock()
          pygame.display.set_caption("TetrisRL")
          pygame.display.set_icon(icon)
     
     def run(self):
          run = True
          while run:
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         run = False

               
               self.screen.fill("purple")
               pygame.display.update()
               self.clock.tick(60)

          pygame.quit()

main = Main()
main.run()