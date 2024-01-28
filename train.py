from getdata import get_data, RESULTDIR, LOGDIR
from dataprocess import pre_cook_data
from datetime import  datetime
from futureenv import FutureEnv
from stable_baselines3 import DDPG


# 获取数据
symbol = "KQ.m@CFFEX.IF" # 合约代码, 天勤中的代码格式, 主力合约必须是 KQ.m@ 开头
data =  get_data(symbol, 60, "test.csv", datetime(2016, 1, 1, 9, 0, 0), datetime(2023, 12, 31, 15,0,0), False)
# 取2023年前的数据
data = data[data.date < datetime(2023, 1, 1, 9, 0, 0).date()]

# 预处理数据, 只取开高低收四个价格和成交量以及时间序列
data = pre_cook_data(data, tech_list=[], tech_para_list={}, origindata=True)

# 初始化期货 env
env = FutureEnv(data)

# 训练模型
model = DDPG("MlpPolicy", 
            buffer_size=1024*4, 
            batch_size=128*4, 
            learning_rate=0.001,
            train_freq=1,
            tau=0.001,
            gamma=0.99,
            policy_kwargs=dict(net_arch=[258, 1024, 258, 258]),
            tensorboard_log=f"{LOGDIR}/ddpg_future_tensorboard/",
            env=env, 
            device="cuda",            
            verbose=1)
model.learn(total_timesteps=1_000_000, log_interval=1)
model.save(f"{RESULTDIR}/ddpg_future.zip")




