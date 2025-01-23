import pygame as pg
from pygame.locals import *
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import random
from collections import deque

# File imports
from world import *
from car import *
from wheel import *
from rendering_functions import *

# Pygame Setup
pg.init()
pg.font.init()
font = pg.font.SysFont('Comic Sans MS', 10)
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
DISPLAY = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 100
clock = pg.time.Clock()
world = World()

# PyTorch Parameters
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001
TRAINING_DELTA_TIME = 0.05

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name = 'model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
    
    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # Get predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            
            target[idx][torch.argmax(action).item()] = Q_new

        # Q_new = reward + gamma * max(next predicted Q value)
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()        

class Agent:
    def __init__(self):
        self.game_count = 0
        self.epsilon = 2 # Randomness
        self.gamma = 0.9 # Discount rate, < 1
        self.memory = deque(maxlen = MAX_MEMORY) # popleft() when memory is exceeded
        self.model = Linear_QNet(5, 256, 4)
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)

        self.model.load_state_dict(torch.load("model/best_model.pth"))

    def get_state(self, game):
        return [
            game.car.angle_to_next_segment,
            game.car.distance_to_next_segment,
            game.car.distance_to_road,
            np.linalg.norm(game.car.velocity),
            game.car.rotational_velocity
        ]

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # Returns list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Random moves: Tradeoff in exploration (random) vs exploitation (model)
        self.epsilon = max(80 - self.game_count, 1)
        final_move = [0, 0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            final_move[random.randint(0, 3)] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move[torch.argmax(prediction).item()] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()

    while True:
        # Get old state
        state_old = agent.get_state(world)

        # Get move
        final_move = agent.get_action(state_old)

        # Perrform move and get new state
        reward, done, score = game_loop(TRAINING_DELTA_TIME, final_move)
        state_new = agent.get_state(world)

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Train long memory
            world.reset()
            agent.game_count += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print(f'Game {agent.game_count}, Score {score}, Record {record}')
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.game_count
            plot_mean_scores.append(mean_score)

            plot(plot_scores, plot_mean_scores)

def game_loop(delta_time, inputs):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                world.debug = not world.debug
            if event.key == pg.K_r:
                world.reset()

    reward, done, score = world.update_world_physics(delta_time, inputs)
    world.update_world_graphics(DISPLAY, font)

    pg.display.update()
    return reward, done, score

while True:
    print("Enter '1' to train model, and '2' for manual control")
    do_train = input("> ")
    if do_train == '1' or do_train == '2':
        break

if int(do_train) == 1:
    train()
else:
    while True:
        keys = pg.key.get_pressed()
        delta_time = clock.tick(FPS) / 1000

        game_loop(
            delta_time,
            (
                keys[pg.K_UP] or keys[pg.K_w],
                keys[pg.K_LEFT] or keys[pg.K_a],
                keys[pg.K_RIGHT] or keys[pg.K_d],
                keys[pg.K_DOWN] or keys[pg.K_s]
            )
        )