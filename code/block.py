import pygame
import random
from settings import BLOCK_SPACE,BLOCK_COLORS

class Block:
    def __init__(self):
        self.tetromino = random.choice(list(BLOCK_COLORS.keys()))
        print(self.tetromino)
        
        
