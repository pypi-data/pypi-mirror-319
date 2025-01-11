
import gymnasium as gym
from evorl import DQNAgent, NormalizedEnv

# Create environment
env = NormalizedEnv(gym.make("CartPole-v1"))

# Create agent
agent = DQNAgent(
    state_dim=env.observation_space.shape[0],
    action_dim=env.action_space.n
)

# Training loop
episodes = 100
for episode in range(episodes):
    obs, _ = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        # Select and perform action
        action = agent.select_action(obs)
        next_obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        
        # Update agent
        agent.update((obs, action, reward, next_obs, done))
        total_reward += reward
        obs = next_obs
    
    if episode % 10 == 0:
        print(f"Episode {episode}: Total Reward = {total_reward}")

# Test the trained agent
agent.eval()
obs, _ = env.reset()
done = False
total_reward = 0

while not done:
    action = agent.select_action(obs)
    obs, reward, terminated, truncated, _ = env.step(action)
    done = terminated or truncated
    total_reward += reward

print(f"
Final evaluation reward: {total_reward}") 
