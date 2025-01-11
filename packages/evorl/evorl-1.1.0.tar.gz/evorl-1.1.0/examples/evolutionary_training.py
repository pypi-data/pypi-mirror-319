
import gymnasium as gym
from evorl import Population, CEM, DQNAgent, NormalizedEnv

# Create environment
env = NormalizedEnv(gym.make("CartPole-v1"))

# Create population with CEM strategy
population = Population(
    agent_class=DQNAgent,
    state_dim=env.observation_space.shape[0],
    action_dim=env.action_space.n,
    population_size=10,
    elite_size=2
)

# Evolution loop
generations = 20
for generation in range(generations):
    # Evaluate population
    metrics = population.evaluate(env, n_episodes=3)
    
    print(f"Generation {generation}:")
    print(f"  Mean Fitness: {metrics['mean_fitness']:.2f}")
    print(f"  Best Fitness: {metrics['best_fitness']:.2f}")
    print(f"  Elite Fitness: {metrics['elite_fitness']:.2f}")
    
    # Create next generation
    strategy = CEM(elite_frac=0.2)
    updates = strategy.compute_updates(
        population.population,
        population.fitness_scores
    )
    population.apply_updates(updates)

# Test best agent
if population.best_agent:
    print("
Testing best agent:")
    obs, _ = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        action = population.best_agent.select_action(obs)
        obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        total_reward += reward
    
    print(f"Final reward: {total_reward}") 
