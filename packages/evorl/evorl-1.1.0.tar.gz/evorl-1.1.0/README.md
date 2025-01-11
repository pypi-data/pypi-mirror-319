
# EvoRL

An evolutionary reinforcement learning framework that combines evolutionary algorithms with deep RL.

[![Website](https://img.shields.io/badge/Website-evorl.ai-blue)](https://evorl.ai)
[![Twitter](https://img.shields.io/badge/Twitter-@EvoLearning-blue)](https://x.com/ReinforceEvo)
[![PyPI version](https://badge.fury.io/py/evorl.svg)](https://badge.fury.io/py/evorl)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🧬 Evolutionary optimization of RL agents
- 🤖 Multiple agent types (DQN, PPO)
- 🔄 Various evolution strategies (CEM, PGPE, NES)
- 📊 Environment normalization and preprocessing
- 🚀 Easy to extend and customize

## Installation

```bash
pip install evorl
```

For development installation with additional tools:
```bash
pip install "evorl[dev]"
```

## Quick Start

### Basic Usage
```python
from evorl import DQNAgent, NormalizedEnv
import gymnasium as gym

# Create environment
env = NormalizedEnv(gym.make("CartPole-v1"))

# Create and train a single agent
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
        action = agent.select_action(obs)
        next_obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        agent.update((obs, action, reward, next_obs, done))
        total_reward += reward
        obs = next_obs

    print(f"Episode {episode}: Reward = {total_reward}")
```

### Evolutionary Training
```python
from evorl import Population, CEM

# Create population of agents
population = Population(
    agent_class=DQNAgent,
    state_dim=env.observation_space.shape[0],
    action_dim=env.action_space.n,
    population_size=10
)

# Create evolution strategy
strategy = CEM(elite_frac=0.2)

# Evolution loop
generations = 20
for generation in range(generations):
    # Evaluate population
    metrics = population.evaluate(env, n_episodes=3)
    print(f"Generation {generation}: Mean Fitness = {metrics['mean_fitness']:.2f}")

    # Create next generation
    updates = strategy.compute_updates(population.population, population.fitness_scores)
    population.apply_updates(updates)
```

## Documentation

For detailed documentation, visit [evorl.ai](https://evorl.ai)

## Available Components

### Agents
- `DQNAgent`: Deep Q-Network implementation
- `PPOAgent`: Proximal Policy Optimization implementation

### Evolution Strategies
- `CEM`: Cross-Entropy Method
- `PGPE`: Policy Gradients with Parameter Exploration
- `NES`: Natural Evolution Strategies

### Environment Wrappers
- `NormalizedEnv`: Observation and reward normalization

## Development

```bash
# Clone the repository
git clone https://github.com/zhangalex1/evorl.git
cd evorl

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=evorl
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details
