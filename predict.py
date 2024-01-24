from getdata import get_data, RESULTDIR
from dataprocess import pre_cook_data
from datetime import datetime
from futureenv import FutureEnv
from stable_baselines3 import DDPG

# 取数据
symbol = "KQ.m@CFFEX.IF"
data =  get_data(symbol, 60, "test.csv", datetime(2023, 12, 1, 9, 0, 0), datetime(2023, 12, 31, 15,0,0), False)

# 预处理数据
data = pre_cook_data(data)

# 初始化期货 env
env = FutureEnv(data)

# 加载模型
model = DDPG.load(f"{RESULTDIR}/ddpg_future.zip", env=env)
obs = env.reset()
rewards = []
steps = len(data)//env.window_size
for i in range(steps):
    action, _ = model.predict(obs)
    obs, reward, done, info = env.step(action)
    rewards.append(reward)    
    if done:
        break        

import matplotlib.pyplot as plt
import numpy
plt.plot(numpy.cumsum(rewards))
plt.show()
plt.plot(data.close.loc[::env.window_size])
plt.show()
