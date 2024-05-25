import pygame
pygame.init()
#window settings
tile_size = 30
collumns = 10
padding = 10
rows = 20
g_width = tile_size * collumns
g_height = tile_size * rows
fall_speed = 500

#menu
m_width = tile_size * 4



#img
#icon = pygame.image.load("trl.png")

#events
MOVE_DOWN_EVENT= pygame.USEREVENT + 1
FALL_SPEED_EVENT= pygame.USEREVENT + 2
NEW_BLOCK_EVENT = pygame.USEREVENT + 3



#blocks
T = "T"
L = "L"
J = "J"
S = "S"
Z = "Z"
O = "O"
I = "I"

BLOCK_COLORS = {
    T : (173, 0, 188),
    L : (233, 113, 0),
    J : (0,0,211),
    S : (125, 255, 4),
    Z : (251, 12, 0),
    O : (251, 236, 0),
    I : (101, 240, 249)
}

BLOCK_SPACE = {
    T : [[[1,1,1],[0,1,0]],[[0,1],[1,1],[0,1]],[[0,1,0],[1,1,1]],[[1,0],[1,1],[1,0]]],
    L : [[[1,1,1],[1,0,0]],[[1,1],[0,1],[0,1]],[[0,0,1],[1,1,1]],[[1,0],[1,0],[1,1]]],
    J : [[[1,0,0],[1,1,1]],[[1,1],[1,0],[1,0]],[[1,1,1],[0,0,1]],[[0,1],[0,1],[1,1]]],
    S : [[[0,1,1],[1,1,0]],[[1,0],[1,1],[0,1]],[[0,1,1],[1,1,0]],[[1,0],[1,1],[0,1]]],
    Z : [[[1,1,0],[0,1,1]],[[0,1],[1,1],[1,0]],[[1,1,0],[0,1,1]],[[0,1],[1,1],[1,0]]],
    O : [[[1,1],[1,1]],[[1,1],[1,1]],[[1,1],[1,1]],[[1,1],[1,1]]],
    I : [[[1,1,1,1]],[[1],[1],[1],[1]],[[1,1,1,1]],[[1],[1],[1],[1]]]
}

