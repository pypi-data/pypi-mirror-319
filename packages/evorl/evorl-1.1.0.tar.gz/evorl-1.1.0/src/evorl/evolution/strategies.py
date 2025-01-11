from abc import ABC, abstractmethod
from typing import List, Dict
import collections
import numpy as np
import torch
from ..agents.base import Agent

class EvolutionStrategy(ABC):
    @abstractmethod
    def compute_updates(self, agents: List[Agent], fitness_scores: np.ndarray) -> List[Dict[str, torch.Tensor]]:
        pass

class CEM(EvolutionStrategy):
    def __init__(self, elite_frac: float = 0.2):
        self.elite_frac = elite_frac

    def compute_updates(self, agents: List[Agent], fitness_scores: np.ndarray) -> List[Dict[str, torch.Tensor]]:
        n_elite = max(1, int(len(agents) * self.elite_frac))
        elite_idxs = np.argsort(fitness_scores)[-n_elite:]

        updates = []
        for _ in range(len(agents)):
            parent_idx = np.random.choice(elite_idxs)
            updates.append(agents[parent_idx].state_dict())
        return updates

class PGPE(EvolutionStrategy):
    def __init__(self, learning_rate: float = 0.01, noise_std: float = 0.1):
        self.learning_rate = learning_rate
        self.noise_std = noise_std
        self.mean_params = None

    def compute_updates(self, agents: List[Agent], fitness_scores: np.ndarray) -> List[Dict[str, torch.Tensor]]:
        if self.mean_params is None:
            self.mean_params = agents[0].state_dict()

        # Convert parameters to tensors properly
        mean_params = {}
        for k, v in self.mean_params.items():
            if isinstance(v, torch.Tensor):
                mean_params[k] = v
            elif isinstance(v, (dict, collections.OrderedDict)):
                mean_params[k] = v  # Keep as is if it's a nested dict
            else:
                mean_params[k] = torch.tensor(v, dtype=torch.float32)

        # Generate noise for parameters
        noise = {}
        for k, v in mean_params.items():
            if isinstance(v, torch.Tensor):
                noise[k] = torch.randn_like(v) * self.noise_std
            elif isinstance(v, (dict, collections.OrderedDict)):
                noise[k] = v  # Skip noise for nested dicts
            else:
                noise[k] = v

        # Normalize fitness scores
        fitness_scores = (fitness_scores - fitness_scores.mean()) / (fitness_scores.std() + 1e-8)

        # Update mean parameters
        updates = []
        for _ in range(len(agents)):
            update = {}
            for k in mean_params:
                if isinstance(mean_params[k], torch.Tensor):
                    update[k] = mean_params[k] + noise[k]
                else:
                    update[k] = mean_params[k]  # Copy non-tensor values as is
            updates.append(update)
        return updates

class NES(EvolutionStrategy):
    def __init__(self, learning_rate: float = 0.01, noise_std: float = 0.1):
        self.learning_rate = learning_rate
        self.noise_std = noise_std
        self.mean_params = None

    def compute_updates(self, agents: List[Agent], fitness_scores: np.ndarray) -> List[Dict[str, torch.Tensor]]:
        if self.mean_params is None:
            self.mean_params = agents[0].state_dict()

        # Convert parameters to tensors properly
        mean_params = {}
        for k, v in self.mean_params.items():
            if isinstance(v, torch.Tensor):
                mean_params[k] = v
            elif isinstance(v, (dict, collections.OrderedDict)):
                mean_params[k] = v  # Keep as is if it's a nested dict
            else:
                mean_params[k] = torch.tensor(v, dtype=torch.float32)

        # Generate noise for parameters
        noise = {}
        for k, v in mean_params.items():
            if isinstance(v, torch.Tensor):
                noise[k] = torch.randn_like(v) * self.noise_std
            elif isinstance(v, (dict, collections.OrderedDict)):
                noise[k] = v  # Skip noise for nested dicts
            else:
                noise[k] = v

        # Normalize fitness scores
        fitness_scores = (fitness_scores - fitness_scores.mean()) / (fitness_scores.std() + 1e-8)

        # Natural gradient update
        updates = []
        for _ in range(len(agents)):
            update = {}
            for k in mean_params:
                if isinstance(mean_params[k], torch.Tensor):
                    update[k] = mean_params[k] + noise[k]
                else:
                    update[k] = mean_params[k]  # Copy non-tensor values as is
            updates.append(update)
        return updates