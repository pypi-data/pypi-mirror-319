
from typing import Type, Dict, Any, Optional, Union
from pathlib import Path
import torch

from .base import Agent
from .dqn import DQNAgent
from .ppo import PPOAgent

AGENT_TYPES = {
    "dqn": DQNAgent,
    "ppo": PPOAgent
}

def create_agent(
    agent_type: str,
    state_dim: int,
    action_dim: int,
    config: Optional[Dict[str, Any]] = None
) -> Agent:
    """Create a new agent instance.
    
    Args:
        agent_type: Type of agent ("dqn" or "ppo")
        state_dim: Dimension of state space
        action_dim: Dimension of action space
        config: Optional configuration dictionary
    
    Returns:
        New agent instance
    """
    if agent_type not in AGENT_TYPES:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    return AGENT_TYPES[agent_type](state_dim, action_dim, config)

def save_agent(agent: Agent, path: Union[str, Path]) -> None:
    """Save agent to disk.
    
    Args:
        agent: Agent instance to save
        path: Path to save to
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    agent.save(path)

def load_agent(
    agent_type: str,
    path: Union[str, Path],
    state_dim: int,
    action_dim: int
) -> Agent:
    """Load agent from disk.
    
    Args:
        agent_type: Type of agent ("dqn" or "ppo") 
        path: Path to load from
        state_dim: Dimension of state space
        action_dim: Dimension of action space
    
    Returns:
        Loaded agent instance
    """
    agent = create_agent(agent_type, state_dim, action_dim)
    agent.load(path)
    return agent 
