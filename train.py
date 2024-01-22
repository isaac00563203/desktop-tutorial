from getdata import getDataFromTqSdk, RESULTDIR, LOGDIR
from dataprocess import *
from collections import namedtuple
from datetime import date, datetime
from futureenv import FutureEnv
from stable_baselines3 import DDPG
import os

symbol = "KQ.m@CFFEX.IF" # 合约代码, 天勤中的代码格式, 主力合约必须是 KQ.m@ 开头

# 取测试的数据 如果没有tq账户，可以用其他接口，代替该函数，数据格式 见 .catche/test.csv
data = getDataFromTqSdk(symbol, 60, "test.csv", datetime(2023, 11, 10, 9, 0, 0), datetime(2023, 11, 15, 15,0,0), False)

# 加入技术指标
data = add_tech_index(data, tech_list=tech_list, tech_para_list=tech_para_list)

# 计算技术指标时，会产生一些Nan值，去掉
data = data.iloc[200:]

# 初始化期货 env
env = FutureEnv(data, window_size=10)

model = DDPG("MlpPolicy", 
            buffer_size=1000, 
            batch_size=100, 
            learning_rate=0.001,
            train_freq=1,
            tau=0.001,
            gamma=0.99,
            policy_kwargs=dict(net_arch=[256, 256]),
            tensorboard_log=f"{LOGDIR}/ddpg_future_tensorboard/",
            env=env, 
            verbose=50)
model.learn(total_timesteps=100000, log_interval=100)
model.save(f"{RESULTDIR}/ddpg_future.zip")



