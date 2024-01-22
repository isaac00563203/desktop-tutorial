import numpy as np
import pandas as pd
from pandas import DataFrame
from gym.utils import seeding
import gym

class FutureEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, data:pd.DataFrame, **kwargs):                
        
        self.steps = 0
        self.max_steps = len(data)

        self.reward = 0
        self.done = False
        self.info = {}
        self.episode = 0
        self.data = data        
                
        self.buy_cost = 0
        self.sell_cost = 0
        
        self.buy_price = 0
        self.sell_price = 0
        
        self.position = 0

        self.price_list = data['close'].tolist()

        self.data = data[['open', 'high', 'low', 'close']] # 'MA5', 'MA10', 'MA20', 'MA30', 'MA60', 'MA120', 'MA240', 'EMA5', 'EMA10', 'EMA20', 'EMA30', 'EMA60', 'EMA120', 'EMA240', 'SAR', 'CCI', 'ATR', 'OBV', 'WILLR', 'AD']]

        self.window_size = kwargs.get('window_size', 10)
        
        self.amount = kwargs.get('amount', 1)
        self.buy_cost_rate = kwargs.get('buy_cost_rate', 0.0000)        
        self.sell_cost_rate = kwargs.get('sell_cost_rate', 0.0000)     

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
        if self.position > 0:            
            return self.pre_price * self.amount * self.sell_cost_rate
        elif self.position < 0:
            return self.pre_price * self.amount * self.buy_cost_rate
        else:
            return 0

    def step(self, action):
        self.pre_price = self.current_price      
        self.state = self.data.iloc[self.steps : self.steps + self.window_size, :].to_numpy()
        
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

        return self.state, reward, self.done, self.info
    
    def reset(self):
        self.steps = 0        
        self.done = False
        self.reward = 0
        
        self.state = self.data.iloc[0 : self.window_size, :].to_numpy()
        self.current_price = self.price_list[self.steps + self.window_size - 1]
        self.episode += 1
        return self.state
    
    def render(self, mode='human', close=False):
        pass

    def seed(self, seed=None):
        _, seed = seeding.np_random(seed)
        return [seed]



