
from abc import ABC, abstractmethod
import torch
import numpy as np
from typing import Dict, Any, Tuple, Optional, Union, List

# Base agent class
class Agent(ABC):
    """Base class for all agents in EvoRL.

    This abstract class defines the interface that all agents must implement.

    Args:
        state_dim: Dimension of the state space
        action_dim: Dimension of the action space
        config: Optional configuration dictionary
    """

    def __init__(self, state_dim: int, action_dim: int, config: Optional[Dict[str, Any]] = None):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.config = config or {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.metrics = {}
        self.training = True

    @abstractmethod
    def select_action(self, state: Union[np.ndarray, torch.Tensor]) -> np.ndarray:
        """Select an action given a state.

        Args:
            state: Current environment state

        Returns:
            Selected action as a numpy array
        """
        pass

    @abstractmethod
    def update(self, experience: Tuple) -> Dict[str, float]:
        """Update the agent using an experience tuple.

        Args:
            experience: Tuple of (state, action, reward, next_state, done)

        Returns:
            Dictionary of metrics from the update
        """
        pass

    @abstractmethod
    def state_dict(self) -> Dict[str, Any]:
        """Get a dictionary of the agent's state.

        Returns:
            Dictionary containing all state information
        """
        pass

    @abstractmethod
    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        """Load a state dictionary into the agent.

        Args:
            state_dict: Dictionary containing state information
        """
        pass

    def train(self) -> None:
        """Set the agent to training mode."""
        self.training = True

    def eval(self) -> None:
        """Set the agent to evaluation mode."""
        self.training = False

    def save(self, path: str) -> None:
        """Save the agent to a file.

        Args:
            path: Path to save the agent to
        """
        torch.save({
            'state_dict': self.state_dict(),
            'config': self.config
        }, path)

    def load(self, path: str) -> None:
        """Load the agent from a file.

        Args:
            path: Path to load the agent from
        """
        checkpoint = torch.load(path, map_location=self.device)
        self.load_state_dict(checkpoint['state_dict'])
        self.config = checkpoint['config']
