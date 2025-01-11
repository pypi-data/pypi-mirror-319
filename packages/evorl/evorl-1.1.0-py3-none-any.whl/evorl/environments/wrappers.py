
import gymnasium as gym
import numpy as np
from typing import Tuple, Dict, Any, Optional
from collections import deque

# Running mean and standard deviation
class RunningMeanStd:
    def __init__(self, shape: Tuple[int, ...]):
        self.mean = np.zeros(shape, dtype=np.float64)
        self.var = np.ones(shape, dtype=np.float64)
        self.count = 0

    def update(self, x: np.ndarray) -> None:
        batch_mean = np.mean(x, axis=0)
        batch_var = np.var(x, axis=0)
        batch_count = x.shape[0]

        delta = batch_mean - self.mean
        tot_count = self.count + batch_count

        new_mean = self.mean + delta * batch_count / tot_count
        m_a = self.var * self.count
        m_b = batch_var * batch_count
        M2 = m_a + m_b + np.square(delta) * self.count * batch_count / tot_count
        new_var = M2 / tot_count

        self.mean = new_mean
        self.var = new_var
        self.count = tot_count

class NormalizedEnv(gym.Wrapper):
    def __init__(
        self,
        env: gym.Env,
        clip_obs: float = 10.0,
        clip_reward: float = 10.0,
        gamma: float = 0.99,
        epsilon: float = 1e-8,
        history_length: int = 1
    ):
        super().__init__(env)
        self.clip_obs = clip_obs
        self.clip_reward = clip_reward
        self.gamma = gamma
        self.epsilon = epsilon
        self.history_length = history_length

        self.obs_rms = RunningMeanStd(shape=self.observation_space.shape)
        self.ret_rms = RunningMeanStd(shape=())
        self.return_acc = 0.0

        # Add observation history for frame stacking
        if history_length > 1:
            self.obs_history = deque(maxlen=history_length)

    def step(self, action) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        obs, reward, terminated, truncated, info = self.env.step(action)

        self.return_acc = self.return_acc * self.gamma + reward
        self.ret_rms.update(np.array([self.return_acc]))

        normalized_obs = self._normalize_obs(obs)
        normalized_reward = self._normalize_reward(reward)

        if hasattr(self, 'obs_history'):
            self.obs_history.append(normalized_obs)
            stacked_obs = np.concatenate(list(self.obs_history))
            normalized_obs = stacked_obs

        if terminated or truncated:
            self.return_acc = 0.0
            if hasattr(self, 'obs_history'):
                self.obs_history.clear()

        return normalized_obs, normalized_reward, terminated, truncated, info

    def reset(self, **kwargs) -> Tuple[np.ndarray, Dict]:
        obs, info = self.env.reset(**kwargs)
        self.return_acc = 0.0
        normalized_obs = self._normalize_obs(obs)

        if hasattr(self, 'obs_history'):
            self.obs_history.clear()
            for _ in range(self.history_length):
                self.obs_history.append(normalized_obs)
            normalized_obs = np.concatenate(list(self.obs_history))

        return normalized_obs, info

    def _normalize_obs(self, obs: np.ndarray) -> np.ndarray:
        self.obs_rms.update(obs.reshape(1, -1))
        normalized = (obs - self.obs_rms.mean) / np.sqrt(self.obs_rms.var + self.epsilon)
        return np.clip(normalized, -self.clip_obs, self.clip_obs)

    def _normalize_reward(self, reward: float) -> float:
        normalized = reward / np.sqrt(self.ret_rms.var + self.epsilon)
        return float(np.clip(normalized, -self.clip_reward, self.clip_reward))
