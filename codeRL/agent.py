import torch
import random
import numpy as np
from collections import deque
from game import TetrisAI
from model import Linear_QNet, QTrainer
from helper import plot
from settings import BLOCK_SPACE

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class TetrisAgent:
    def __init__(self):
        self.num_of_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()

        self.model = Linear_QNet(214, 256, 5)  # Adjusted input size based on the state representation
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        state = []

        # Add the current board state
        for row in game.board.grid:
            for cell in row:
                state.append(cell)

        # Add the current piece's shape and position
        piece_shape = game.block.tetrominoSpace
        piece_x = game.block.x
        piece_y = game.block.y

        # Flatten the shape and add to state
        for row in piece_shape:
            for cell in row:
                state.append(cell)
        
        # Add position information
        state.append(piece_x)
        state.append(piece_y)

        # Add the next piece information
        next_piece_shape = BLOCK_SPACE[game.next_block_letter][0]  # Assuming the next piece in its initial rotation
        for row in next_piece_shape:
            for cell in row:
                state.append(cell)
        
        while len(state) < 214:
            state.append(0)

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.num_of_games
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 4)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        return move

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

            print('Game', agent.num_of_games, 'Score', score, 'Record', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.num_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()