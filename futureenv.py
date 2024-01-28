import numpy as np
import pandas as pd
from pandas import DataFrame
from gym.utils import seeding
import gym

class FutureEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, data:DataFrame, **kwargs):                                
        self.episode : int = 0
        self.data : DataFrame = data
        self.max_steps : int = len(data) 
        self.price_list : list = data['close'].tolist()
        
        # self.data 只取 n_ 开头的列
        self.data = data.filter(regex='^n_')        
        
        self.window_size : int = kwargs.get('window_size', 30)      
        self.amount : int = kwargs.get('amount', 1)
        self.buy_cost_rate : float = kwargs.get('buy_cost_rate', 0.0000)        
        self.sell_cost_rate : float = kwargs.get('sell_cost_rate', 0.0000)     

        self.shape = (self.window_size, self.data.shape[1])
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=self.shape, dtype=np.float32)

        self.reset()   

    def _buy(self):
        reward = (self.current_price - self.pre_price)*self.amount
        if self.position == 0:
            reward -= self.pre_price * self.amount * self.buy_cost_rate
        elif self.position < 0:
            reward -= 2 *self.pre_price * self.amount * self.buy_cost_rate
        return reward

    def _sell(self):
        reward = (self.pre_price - self.current_price)*self.amount
        if self.position == 0:
            reward -= self.pre_price * self.amount * self.sell_cost_rate
        elif self.position > 0:
            reward -= 2 *self.pre_price * self.amount * self.sell_cost_rate
        return reward

    def _close_position(self):        
        reward = 0
        if self.position > 0:            
            reward -= self.pre_price * self.amount * self.sell_cost_rate
        elif self.position < 0:
            reward -= self.pre_price * self.amount * self.buy_cost_rate
        return reward

    def step(self, action):
        self.pre_price = self.current_price  

        obs = self.data.iloc[self.steps : self.steps + self.window_size, :].to_numpy()
        
        self.steps += self.window_size
        self.current_price = self.price_list[self.steps - 1]
        
        action = np.argmax(action)
        if action == 0:
            reward = self._close_position()
            self.position = 0
        elif action == 1:  # buy
            reward = self._buy()
            self.position = 1
        elif action == 2:  # sell
            reward = self._sell()
            self.position = -1
        else:
            raise ValueError("Invalid action {}".format(action))

        if self.steps >= self.max_steps - self.window_size:
            self.done = True

        return obs, reward, self.done, self.info
    
    def reset(self):
        self.position = 0
        self.info = {}
        self.steps = 0        
        self.done = False
        self.reward = 0                
        self.current_price = self.price_list[self.window_size - 1] # 这个价格容易引起歧义
        self.episode += 1
        
        obs = self.data.iloc[0 : self.window_size, :].to_numpy()
        return obs

    def seed(self, seed=None):
        _, seed = seeding.np_random(seed)
        return [seed]



