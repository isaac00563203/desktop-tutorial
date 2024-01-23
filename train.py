from getdata import get_data, RESULTDIR, LOGDIR
from dataprocess import add_tech_index, tech_list, tech_para_list
from datetime import  datetime
from futureenv import FutureEnv
from stable_baselines3 import DDPG

symbol = "KQ.m@CFFEX.IF" # 合约代码, 天勤中的代码格式, 主力合约必须是 KQ.m@ 开头
start_dt = datetime(2023, 1, 1, 9, 0, 0)
end_dt = datetime(2023, 1, 30, 15,0,0)
period = 60
data_csv_filename = "test.csv"

data = get_data(symbol, period, data_csv_filename,  reload=False)


# 加入技术指标
data = add_tech_index(data, tech_list=tech_list, tech_para_list=tech_para_list)



# 计算技术指标时，会产生一些Nan值，去掉
data = data.iloc[240:]

# 初始化期货 env
env = FutureEnv(data)

model = DDPG("MlpPolicy", 
            buffer_size=2048, 
            batch_size=128*2, 
            learning_rate=0.001,
            train_freq=1,
            tau=0.001,
            gamma=0.99,
            policy_kwargs=dict(net_arch=[256*4, 256]),
            tensorboard_log=f"{LOGDIR}/ddpg_future_tensorboard/",
            env=env, 
            verbose=100)
model.learn(total_timesteps=500_000, log_interval=100)
model.save(f"{RESULTDIR}/ddpg_future.zip")



