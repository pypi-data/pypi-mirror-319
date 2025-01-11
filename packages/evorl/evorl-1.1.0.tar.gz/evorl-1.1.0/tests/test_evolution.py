
import pytest
import numpy as np
import gymnasium as gym
from evorl import Population, CEM, PGPE, NES, DQNAgent

def test_population_initialization():
    population = Population(DQNAgent, 4, 2, population_size=5)
    assert len(population.population) == 5
    assert all(isinstance(agent, DQNAgent) for agent in population.population)

def test_cem_strategy():
    strategy = CEM(elite_frac=0.2)
    agents = [DQNAgent(4, 2) for _ in range(5)]
    fitness_scores = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    updates = strategy.compute_updates(agents, fitness_scores)
    assert len(updates) == len(agents)

def test_pgpe_strategy():
    strategy = PGPE(learning_rate=0.01)
    agents = [DQNAgent(4, 2) for _ in range(5)]
    fitness_scores = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    updates = strategy.compute_updates(agents, fitness_scores)
    assert len(updates) == len(agents)

def test_nes_strategy():
    strategy = NES(learning_rate=0.01)
    agents = [DQNAgent(4, 2) for _ in range(5)]
    fitness_scores = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    updates = strategy.compute_updates(agents, fitness_scores)
    assert len(updates) == len(agents)

def test_population_evaluation():
    env = gym.make("CartPole-v1")
    population = Population(DQNAgent, 4, 2, population_size=3)
    metrics = population.evaluate(env, n_episodes=2)
    
    assert 'mean_fitness' in metrics
    assert 'best_fitness' in metrics
    assert 'elite_fitness' in metrics
    assert len(population.history['mean_fitness']) == 1

def test_evolution_strategies():
    agents = [DQNAgent(4, 2) for _ in range(3)]
    fitness_scores = np.array([1.0, 2.0, 3.0])
    
    strategies = [
        CEM(elite_frac=0.3),
        PGPE(learning_rate=0.01),
        NES(learning_rate=0.01)
    ]
    
    for strategy in strategies:
        updates = strategy.compute_updates(agents, fitness_scores)
        assert len(updates) == len(agents)
        assert all(isinstance(update, dict) for update in updates)
