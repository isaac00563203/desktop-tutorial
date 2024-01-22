from getdata import getDataFromTqSdk, RESULTDIR
from datetime import datetime
from futureenv import FutureEnv
from stable_baselines3 import DDPG

symbol = "KQ.m@CFFEX.IF"
data = getDataFromTqSdk(symbol, 60, "test.csv", datetime(2023, 11, 10, 9, 0, 0), datetime(2023, 11, 15, 15,0,0), False)
data = data[200:]
env = FutureEnv(data)
model = DDPG.load(f"{RESULTDIR}/ddpg_future.zip", env=env)
obs = env.reset()
rewards = []
for i in range(1000):
    action, _ = model.predict(obs)
    obs, reward, done, info = env.step(action)
    rewards.append(reward)    
    if done:
        break        

import matplotlib.pyplot as plt
import numpy
plt.plot(numpy.cumsum(rewards))
plt.show()
plt.plot(data.close[200:1200])
plt.show()
