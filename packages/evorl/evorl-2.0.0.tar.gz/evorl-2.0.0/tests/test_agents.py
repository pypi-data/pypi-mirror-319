
import pytest
import torch
import numpy as np
from evorl import DQNAgent, PPOAgent

def test_dqn_agent_initialization():
    agent = DQNAgent(state_dim=4, action_dim=2)
    assert agent.state_dim == 4
    assert agent.action_dim == 2

def test_ppo_agent_initialization():
    agent = PPOAgent(state_dim=4, action_dim=2)
    assert agent.state_dim == 4
    assert agent.action_dim == 2

def test_agent_action_selection():
    agent = DQNAgent(state_dim=4, action_dim=2)
    state = np.random.rand(4)
    action = agent.select_action(state)
    assert isinstance(action, np.ndarray)
    assert action.shape == () or action.shape == (1,)
