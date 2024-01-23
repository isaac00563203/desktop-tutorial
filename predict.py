from getdata import getDataFromTqSdk, RESULTDIR
from datetime import datetime
from futureenv import FutureEnv
from stable_baselines3 import DDPG

symbol = "KQ.m@CFFEX.IF"
data = getDataFromTqSdk(symbol, 60, "test.csv", datetime(2023, 12, 1, 9, 0, 0), datetime(2023, 12, 31, 15,0,0), False)
data = data[240:]
env = FutureEnv(data)
model = DDPG.load(f"{RESULTDIR}/ddpg_future.zip", env=env)
obs = env.reset()
rewards = []
eph = len(data)//env.window_size
for i in range(eph):
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
