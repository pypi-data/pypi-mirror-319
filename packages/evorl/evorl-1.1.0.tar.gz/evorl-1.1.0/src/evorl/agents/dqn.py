import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from typing import Dict, Any, Tuple, List, Optional, Union
from collections import deque
import random

from .base import Agent


class DQNAgent(Agent):
    """Deep Q-Network agent implementation.

    Args:
        state_dim: Dimension of the state space
        action_dim: Dimension of the action space
        config: Optional configuration dictionary with hyperparameters:
            - batch_size: Size of training batches (default: 64)
            - gamma: Discount factor (default: 0.99)
            - target_update_freq: Target network update frequency (default: 100)
            - lr: Learning rate (default: 3e-4)
            - buffer_size: Size of replay buffer (default: 100000)
    """

    # Default configuration
    def __init__(self, state_dim: int, action_dim: int, config: Optional[Dict[str, Any]] = None):
        super().__init__(state_dim, action_dim, config)

        # Network architecture
        hidden_dims = self.config.get('hidden_dims', [256, 128])
        layers = []
        prev_dim = state_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU()
            ])
            prev_dim = hidden_dim
        layers.append(nn.Linear(prev_dim, action_dim))

        self.network = nn.Sequential(*layers).to(self.device)
        self.target_network = nn.Sequential(*layers).to(self.device)

        # Initialize target network
        self.target_network.load_state_dict(self.network.state_dict())

        # Training parameters
        lr = self.config.get('lr', 3e-4)
        self.optimizer = optim.Adam(self.network.parameters(), lr=lr)
        self.buffer = deque(maxlen=self.config.get('buffer_size', 100000))
        self.batch_size = self.config.get('batch_size', 64)
        self.gamma = self.config.get('gamma', 0.99)
        self.target_update_freq = self.config.get('target_update_freq', 100)
        self.update_count = 0

    def select_action(self, state: Union[np.ndarray, torch.Tensor]) -> np.ndarray:
        """Select an action using epsilon-greedy policy."""
        epsilon = 0.01 if not self.training else max(0.01, 1.0 - self.update_count / 10000)
        if random.random() < epsilon:
            return np.array(np.random.randint(self.action_dim))

        with torch.no_grad():
            if isinstance(state, np.ndarray):
                state = torch.FloatTensor(state).to(self.device)
            q_values = self.network(state)
            return np.array(q_values.argmax().cpu().numpy())

    def update(self, experience: Tuple) -> Dict[str, float]:
        """Update the agent using DQN algorithm."""
        state, action, reward, next_state, done = experience
        # Convert experience to numpy arrays if they aren't already
        state = np.asarray(state)
        next_state = np.asarray(next_state)

        # Store experience as tuple of numpy arrays
        self.buffer.append((state, action, reward, next_state, done))
        self.update_count += 1

        if len(self.buffer) < self.batch_size:
            return {"loss": 0.0}

        # Sample batch and convert to tensors
        batch = random.sample(self.buffer, self.batch_size)

        # Stack arrays before converting to tensors for efficiency
        states = np.stack([x[0] for x in batch])
        actions = np.array([x[1] for x in batch])
        rewards = np.array([x[2] for x in batch])
        next_states = np.stack([x[3] for x in batch])
        dones = np.array([x[4] for x in batch])

        # Convert to tensors
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        # Compute Q values
        current_q = self.network(states).gather(1, actions.unsqueeze(1))
        next_q = self.target_network(next_states).max(1)[0].detach()
        target_q = rewards + (1 - dones) * self.gamma * next_q

        # Compute loss and update
        loss = F.mse_loss(current_q.squeeze(), target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Update target network
        if self.update_count % self.target_update_freq == 0:
            self.target_network.load_state_dict(self.network.state_dict())

        return {"loss": loss.item()}

    def state_dict(self) -> Dict[str, Any]:
        return {
            'network': self.network.state_dict(),
            'target_network': self.target_network.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'update_count': self.update_count
        }

    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        self.network.load_state_dict(state_dict['network'])
        self.target_network.load_state_dict(state_dict['target_network'])
        self.optimizer.load_state_dict(state_dict['optimizer'])
        self.update_count = state_dict['update_count']