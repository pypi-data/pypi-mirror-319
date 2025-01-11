
from pathlib import Path
from typing import List, Type, Dict, Any, Optional, Union
import numpy as np
import torch
import copy
from ..agents.base import Agent

class Population:
    """A population of agents for evolutionary optimization.

    Args:
        agent_class: Class of agents to create
        state_dim: Dimension of state space
        action_dim: Dimension of action space
        population_size: Number of agents in population
        elite_size: Number of elite agents to preserve
        mutation_rate: Rate of random mutations
        config: Optional configuration for agents
    """

    def __init__(
        self,
        agent_class: Type[Agent],
        state_dim: int,
        action_dim: int,
        population_size: int = 10,
        elite_size: int = 2,
        mutation_rate: float = 0.1,
        config: Optional[Dict[str, Any]] = None
    ):
        self.agent_class = agent_class
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.config = config or {}
        
        self.generation = 0
        self.history = {
            'mean_fitness': [],
            'best_fitness': [],
            'elite_fitness': []
        }

        self.population = [
            agent_class(state_dim, action_dim, self.config)
            for _ in range(population_size)
        ]
        self.fitness_scores = np.zeros(population_size)
        self.best_fitness = float('-inf')
        self.best_agent = None

    # Evaluation, selection, and update methods
    def evaluate(self, env, n_episodes: int = 1) -> Dict[str, float]:
        """Evaluate all agents in the population.

        Args:
            env: Gymnasium environment
            n_episodes: Number of episodes per evaluation

        Returns:
            Dictionary of evaluation metrics
        """
        for i, agent in enumerate(self.population):
            total_reward = 0
            for _ in range(n_episodes):
                obs, _ = env.reset()
                done = False
                while not done:
                    action = agent.select_action(obs)
                    obs, reward, terminated, truncated, _ = env.step(action)
                    total_reward += reward
                    done = terminated or truncated

            self.fitness_scores[i] = total_reward / n_episodes
            if self.fitness_scores[i] > self.best_fitness:
                self.best_fitness = self.fitness_scores[i]
                self.best_agent = copy.deepcopy(agent)

        # Update history
        elite_fitness = np.mean(np.sort(self.fitness_scores)[-self.elite_size:])
        self.history['mean_fitness'].append(float(np.mean(self.fitness_scores)))
        self.history['best_fitness'].append(float(self.best_fitness))
        self.history['elite_fitness'].append(float(elite_fitness))

        return {
            'generation': self.generation,
            'mean_fitness': self.history['mean_fitness'][-1],
            'best_fitness': self.best_fitness,
            'elite_fitness': elite_fitness
        }

    def apply_updates(self, updates: List[Dict[str, torch.Tensor]]) -> None:
        """Apply parameter updates to the population."""
        for agent, update in zip(self.population, updates):
            agent.load_state_dict(update)
        self.generation += 1

    def save(self, path: Union[str, Path]) -> None:
        """Save population state to disk."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        state = {
            'config': self.config,
            'generation': self.generation,
            'best_fitness': self.best_fitness,
            'history': self.history,
            'population': [agent.state_dict() for agent in self.population]
        }
        if self.best_agent is not None:
            state['best_agent'] = self.best_agent.state_dict()

        torch.save(state, path)

    def load(self, path: Union[str, Path]) -> None:
        """Load population state from disk."""
        state = torch.load(path)

        self.config = state['config']
        self.generation = state['generation']
        self.best_fitness = state['best_fitness']
        self.history = state['history']

        for agent, agent_state in zip(self.population, state['population']):
            agent.load_state_dict(agent_state)

        if 'best_agent' in state and state['best_agent'] is not None:
            self.best_agent = copy.deepcopy(self.population[0])
            self.best_agent.load_state_dict(state['best_agent'])
