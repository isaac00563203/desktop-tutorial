from getdata import getDataFromTqSdk, RESULTDIR, LOGDIR
from pandas import DataFrame, Series
from collections import namedtuple
from datetime import date, datetime
from futureenv import FutureEnv
from stable_baselines3 import PPO,DDPG
import os

symbol = "KQ.m@CFFEX.IF" # 合约代码, 天勤中的代码格式, 主力合约必须是 KQ.m@ 开头
data = getDataFromTqSdk(symbol, 60, "test.csv", datetime(2023, 11, 10, 9, 0, 0), datetime(2023, 11, 15, 15,0,0), False)
env = FutureEnv(data, window_size=10)
model = DDPG("MlpPolicy", 
            buffer_size=1000, 
            batch_size=100, 
            learning_rate=0.001,
            train_freq=1,
            tau=0.001,
            gamma=0.98,
            policy_kwargs=dict(net_arch=[256, 256]),
            tensorboard_log=f"{LOGDIR}/ddpg_future_tensorboard/",
            env=env, 
            verbose=50)
model.learn(total_timesteps=100000, log_interval=100)
model.save(f"{RESULTDIR}/ddpg_future.zip")



