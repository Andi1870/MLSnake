# train.py
from snake.environment import SnakeEnv
from agent.dqn_agent import DQNAgent
import numpy as np

env = SnakeEnv()
agent = DQNAgent(state_size=6, action_size=3)  # 6 Features, 3 Aktionen (links, gerade, rechts)

episodes = 1000
for ep in range(episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        agent.remember(state, action, reward, next_state, done)
        agent.replay()
        state = next_state
        total_reward += reward

    print(f"Episode {ep+1}: Total reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.3f}")
