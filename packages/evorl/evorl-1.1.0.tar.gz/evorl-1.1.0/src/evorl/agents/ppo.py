
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from typing import Dict, Any, Tuple, List, Optional, Union
from collections import deque

from .base import Agent

class PPONetwork(nn.Module):
    """PPO network architecture with shared features, policy and value heads.

    Args:
        state_dim: Dimension of the state space
        action_dim: Dimension of the action space
        hidden_dims: List of hidden layer dimensions
    """
    def __init__(self, state_dim: int, action_dim: int, hidden_dims: List[int] = [256, 128]):
        super().__init__()
        layers = []
        prev_dim = state_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.Tanh()
            ])
            prev_dim = hidden_dim

        self.shared = nn.Sequential(*layers)
        self.policy = nn.Linear(prev_dim, action_dim)
        self.value = nn.Linear(prev_dim, 1)
        self.log_std = nn.Parameter(torch.zeros(action_dim))

    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        features = self.shared(state)
        return self.policy(features), self.value(features)

    def get_distribution(self, state: torch.Tensor) -> torch.distributions.Normal:
        mean, _ = self.forward(state)
        std = self.log_std.exp()
        return torch.distributions.Normal(mean, std)

# PPO agent implementation
class PPOAgent(Agent):
    """Proximal Policy Optimization agent implementation.

    Args:
        state_dim: Dimension of the state space
        action_dim: Dimension of the action space
        config: Optional configuration dictionary with hyperparameters:
            - hidden_dims: List of hidden layer dimensions (default: [256, 128])
            - lr: Learning rate (default: 3e-4)
            - clip_ratio: PPO clip ratio (default: 0.2)
            - value_coef: Value loss coefficient (default: 0.5)
            - entropy_coef: Entropy bonus coefficient (default: 0.01)
    """

    def __init__(self, state_dim: int, action_dim: int, config: Optional[Dict[str, Any]] = None):
        super().__init__(state_dim, action_dim, config)
        hidden_dims = self.config.get('hidden_dims', [256, 128])
        self.network = PPONetwork(state_dim, action_dim, hidden_dims).to(self.device)

        # Training parameters
        lr = self.config.get('lr', 3e-4)
        self.optimizer = optim.Adam(self.network.parameters(), lr=lr)
        self.clip_ratio = self.config.get('clip_ratio', 0.2)
        self.value_coef = self.config.get('value_coef', 0.5)
        self.entropy_coef = self.config.get('entropy_coef', 0.01)

        # Experience buffer
        self.buffer = deque(maxlen=2048)

    def select_action(self, state: Union[np.ndarray, torch.Tensor]) -> np.ndarray:
        """Select an action using the current policy."""
        with torch.no_grad():
            if isinstance(state, np.ndarray):
                state = torch.FloatTensor(state).to(self.device)
            dist = self.network.get_distribution(state)
            if self.training:
                action = dist.sample()
            else:
                action = dist.mean
            return action.cpu().numpy()

    def update(self, experience: Tuple) -> Dict[str, float]:
        """Update the agent using PPO algorithm."""
        state, action, reward, next_state, done = experience
        self.buffer.append(experience)

        if len(self.buffer) < 64:  # Minimum batch size
            return {"loss": 0.0}

        # Prepare batch
        batch = list(self.buffer)
        states = torch.FloatTensor([x[0] for x in batch]).to(self.device)
        actions = torch.FloatTensor([x[1] for x in batch]).to(self.device)
        rewards = torch.FloatTensor([x[2] for x in batch]).to(self.device)

        # Get current policy distribution and values
        dist = self.network.get_distribution(states)
        values = self.network(states)[1]

        # Compute losses
        policy_loss = -dist.log_prob(actions).mean()
        value_loss = F.mse_loss(values.squeeze(), rewards)
        entropy_loss = -dist.entropy().mean()

        # Compute total loss with coefficients
        loss = (
            policy_loss + 
            self.value_coef * value_loss + 
            self.entropy_coef * entropy_loss
        )

        # Update network
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return {
            "loss": loss.item(),
            "policy_loss": policy_loss.item(),
            "value_loss": value_loss.item(),
            "entropy": -entropy_loss.item()
        }

    def state_dict(self) -> Dict[str, Any]:
        return {
            'network': self.network.state_dict(),
            'optimizer': self.optimizer.state_dict()
        }

    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        self.network.load_state_dict(state_dict['network'])
        self.optimizer.load_state_dict(state_dict['optimizer'])
