
import pytest
import gymnasium as gym
import numpy as np
from evorl import NormalizedEnv

@pytest.fixture
def env():
    return NormalizedEnv(gym.make('CartPole-v1'))

def test_normalized_env_initialization(env):
    assert hasattr(env, 'obs_rms')
    assert hasattr(env, 'ret_rms')
    assert hasattr(env, 'clip_obs')
    assert hasattr(env, 'clip_reward')

def test_normalized_env_step(env):
    obs, _ = env.reset()
    assert isinstance(obs, np.ndarray)
    action = env.action_space.sample()
    obs, reward, done, truncated, info = env.step(action)
    assert isinstance(obs, np.ndarray)
    assert isinstance(reward, float)
