import torch as T
import numpy as np
import random as r
from collections import deque
from model import Linear_QNet, QTrainer
from helper import plot
from game import TetrisAI
from settings import BLOCK_SPACE

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class TetrisAgent:
    def __init__(self):
        self.num_of_games = 0
        self.epsilon = 1.0  
        self.min_epsilon = 0.01  
        self.epsilon_decay = 0.995  
        self.gamma = 0.99
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(4, 256, 5) 
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        state = []
        
        state.append(game.board.numberOfHoles())
        state.append(game.board.calculateBumpiness())
        state.append(self.get_lines_cleared(game.board))
        state.append(self.get_total_height(game.board))

        return np.array(state, dtype=float)

    def get_lines_cleared(self, board):
        cleared_lines = 0
        for row in board.grid:
            if all(cell != 0 for cell in row):
                cleared_lines += 1
        return cleared_lines

    def get_total_height(self, board):
        heights = [0] * board.collumns
        for x in range(board.collumns):
            for y in range(board.rows):
                if board.grid[y][x] == 1:
                    heights[x] = board.rows - y
                    break
        return sum(heights)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = r.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        if r.random() < self.epsilon:
            move = r.randint(0, 4)
        else:
            state0 = T.tensor(state, dtype=T.float)
            prediction = self.model(state0)
            move = T.argmax(prediction).item()

        return move
    
    def update_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = TetrisAgent()
    game = TetrisAI()
    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.playstep(final_move)

        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.num_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.num_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores, record)

            agent.update_epsilon()

if __name__ == '__main__':
    train()
