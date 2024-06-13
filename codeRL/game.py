from settings import *
from board import Board
from block import Block
import random
import pygame
import torch
import numpy as np

class TetrisAI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((g_width + m_width + padding * 3, g_height + padding * 2))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("TetrisRL")

        self.game_space = pygame.Surface((g_width, g_height))
        self.menu_space = pygame.Surface((m_width, g_height))

        self.fall_speed = fall_speed
        self.timer_event = pygame.time.set_timer(MOVE_DOWN_EVENT, fall_speed)
        self.game_over = False
        self.next_block_letter = random.choice(list(BLOCK_COLORS.keys()))

        self.points = 0
        self.downDelay = 10
        self.reset()

    def reset(self):
        self.game_over = False
        self.board = Board(rows, collumns)
        self.block = Block()
        self.points = 0
        self.est_time = 0
        self.frame_iteration = 0
        self.reward = 0
        return self.get_state_properties(self.board)

    def get_state_properties(self, board):
        lines_cleared, board = self.check_cleared_rows(board)
        holes = self.get_holes(board)
        bumpiness, height = self.get_bumpiness_and_height(board)

        return torch.FloatTensor([lines_cleared, holes, bumpiness, height])

    def get_holes(self, board):
        num_holes = 0
        for col in zip(*board.grid):
            row = 0
            while row < self.board.rows and col[row] == 0:
                row += 1
            num_holes += len([x for x in col[row + 1:] if x == 0])
        return num_holes

    def get_bumpiness_and_height(self, board):
        board = np.array(board.grid)
        mask = board != 0
        invert_heights = np.where(mask.any(axis=0), np.argmax(mask, axis=0), self.board.rows)
        heights = self.board.rows - invert_heights
        total_height = np.sum(heights)
        currs = heights[:-1]
        nexts = heights[1:]
        diffs = np.abs(currs - nexts)
        total_bumpiness = np.sum(diffs)
        return total_bumpiness, total_height

    def check_cleared_rows(self, board):
        to_delete = []
        for i, row in enumerate(board.grid[::-1]):
            if 0 not in row:
                to_delete.append(len(board.grid) - 1 - i)
        if len(to_delete) > 0:
            board = self.remove_row(board, to_delete)
        return len(to_delete), board

    def remove_row(self, board, indices):
        for i in indices[::-1]:
            del board.grid[i]
            board.grid = [[0 for _ in range(self.board.collumns)]] + board.grid
        return board

    def playstep(self, action):
        self.frame_iteration += 1
        self.reward = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == MOVE_DOWN_EVENT:
                self.move(2)

        self.move(action)

        if self.game_over:
            self.reward = -10
            print(self.reward)
            return self.reward, self.game_over, self.points

        self.updateUI()
        self.checkCollision()

        pygame.display.update()
        self.clock.tick(60)

        print (self.reward)
        return self.reward, self.game_over, self.points

    def move(self, action):
        if self.block.checkDownCollison(self.board):
            self.checkTetris()
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
            
            self.checkTetris()
            self.newBlock()

    def checkTetris(self):
            points_received = self.block.y
            tetris_counter = 0
            i = len(self.board.grid) - 1
            while i >= 0:
                if self.board.grid[i].count(1) == len(self.board.grid[0]):
                    del self.board.grid[i]
                    tetris_counter += 1
                    del self.board.gridColors[i]
                    self.board.grid.insert(0, [0] * self.board.collumns)
                    self.board.gridColors.insert(0, [0] * self.board.collumns)
                    i = len(self.board.grid) - 1
                else:
                    i -= 1

            if tetris_counter == 1:
                points_received += 100
            elif tetris_counter == 2:
                points_received += 300
            elif tetris_counter == 3:
                points_received += 500
            elif tetris_counter == 4:
                points_received += 800

            self.points += points_received
            if tetris_counter > 0:
                self.reward = 10 * tetris_counter

    def newBlock(self):
        self.board.updateTemplate()
        self.block = Block(self.next_block_letter)
        self.next_block_letter = random.choice(list(BLOCK_COLORS.keys()))
        if self.block.checkNewBlockCollision(self.board):
            self.game_over = True
        else:
            self.block.drawBlock(self.board)
        

    def updateUI(self):
        self.screen.fill((186, 0, 216))
        self.screen.blit(self.game_space, (10, 10))
        self.screen.blit(self.menu_space, (g_width + padding*2 , 10))

        self.draw_text("NEXT", (g_width + padding*2 + m_width //2), 40, 20, True)
        self.draw_text("SCORE", (g_width + padding*2 + m_width //2), self.menu_space.get_height() //2-100, 20, True)
        self.draw_text(str(self.points), (g_width + padding*2 + m_width //2), self.menu_space.get_height() //2 -60, 20, True)
        self.board.drawNextBlock(self.screen, self.next_block_letter, (g_width + padding*2 + m_width //2)-60, 80)

        self.game_space.fill((6,212,150))
        self.menu_space.fill((214,69,80))
        self.board.draw(self.game_space)

    def draw_text(self, text, x, y, size, background):
        font = pygame.font.SysFont("arialblack", size)
        text_color = (0,0,0)

        img = font.render(text, True, text_color)
        text_rect = img.get_rect(center=(x, y))

        if background:
            border_width = 3
            border_rect = pygame.Rect(text_rect.left - border_width, text_rect.top - border_width, text_rect.width + 2 * border_width, text_rect.height + 2 * border_width)
            pygame.draw.rect(self.screen, (0,0,0), border_rect)
            pygame.draw.rect(self.screen, (147,129,255), text_rect)

        self.screen.blit(img, text_rect)

    def newBlock(self):
        self.board.updateTemplate()
        holes = self.board.numberOfHoles()
        bumpiness = self.board.calculateBumpiness()
        # self.reward = -1 * holes - 0.1 * bumpiness
        self.block = Block(self.next_block_letter)
        self.next_block_letter = random.choice(list(BLOCK_COLORS.keys()))
        if self.block.checkNewBlockCollision(self.board):
            self.game_over = True
        else:
            self.block.drawBlock(self.board)

    def checkCollision(self):
        if self.block.checkDownCollison(self.board):
            if self.downDelay <0:
                self.checkTetris()
                self.newBlock()
                self.downDelay = 10
            else:
                self.downDelay -=1
