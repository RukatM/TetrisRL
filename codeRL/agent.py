import torch
import random
import numpy as np
from game import TetrisAI
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.num_of_games = 0
        self.epsilon = 0 #kontrola losowości
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = None
        self.trainer = None


    def get_state(self,game):
        grid = np.array(game.board.grid).flatten()
        current_block = np.array(game.block.tetrominoSpace).flatten()
        block_position = np.array([game.block.x, game.block.y])
        next_block = np.array([ord(game.next_block_letter)])  

        return np.concatenate((grid, current_block, block_position, next_block))
    

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, next_states,dones = zip(*mini_sample)
        self.train_short_memory(states, actions, next_states,dones)

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(self,state,action,reward,next_state,done)

    def get_action(self,state):
        self.epsilon = 80 - self.n_games
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
    agent = Agent()
    game = TetrisAI()
    while True:
        state_old = agent.get_state(game)
    
        final_move = agent.get_action(state_old)

        reward,done,score = game.playstep(final_move)

        state_new = agent.get_state(game)

        agent.train_short_memory(state_old,final_move,reward,state_new,done)

        agent.remember(state_old,final_move,reward,state_new,done)

        if done:
            game.reset()
            agent.num_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
            print('Game', agent.num_of_games,'Score',score,'Record',record)

if __name__ == '__main__':
    train()