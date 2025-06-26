import random
import numpy as np

CELL_SIZE = 20
WIDTH, HEIGHT = 600, 400
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

class SnakeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(5, 5)]  # Startposition im Grid
        self.direction = (1, 0)  # Start Richtung: rechts
        self.spawn_food()
        self.score = 0
        self.done = False
        return self.get_observation()

    def step(self, action):
        if self.done:
            return self.get_observation(), 0, True, {}

        self.change_direction(action)
        new_head = (self.snake[0][0] + self.direction[0],
                    self.snake[0][1] + self.direction[1])

        # Check Kollision mit Wand
        if (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake
        ):
            self.done = True
            return self.get_observation(), -10, True, {}

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.spawn_food()
            reward = 10
        else:
            self.snake.pop()
            reward = -0.1  # leichter Anreiz sich zu bewegen

        return self.get_observation(), reward, self.done, {}

    def spawn_food(self):
        while True:
            self.food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if self.food not in self.snake:
                break

    def change_direction(self, action):
        # 0: links, 1: gerade, 2: rechts
        dir_x, dir_y = self.direction
        if action == 0:  # links
            self.direction = (-dir_y, dir_x)
        elif action == 2:  # rechts
            self.direction = (dir_y, -dir_x)
        # bei 1 (gerade) bleibt Richtung gleich

    def get_observation(self):
        # Einfaches Feature-Array (du kannst später auch Grids zurückgeben)
        head = self.snake[0]
        food_dir = (
            np.sign(self.food[0] - head[0]),
            np.sign(self.food[1] - head[1])
        )
        return np.array([
            head[0], head[1],
            self.direction[0], self.direction[1],
            food_dir[0], food_dir[1]
        ], dtype=np.float32)

    def render(self):
        # Optional: debug-Rendering mit print
        print(f"Snake: {self.snake}, Food: {self.food}")
