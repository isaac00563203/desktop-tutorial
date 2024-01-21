from localconfig import tqsdkuser, tqsdkpassword
from datetime import date, datetime 
import pandas as pd
from pandas import DataFrame, Series
from collections import namedtuple
import os

CACHDIR = ".cache"
if not os.path.exists(CACHDIR):
    os.mkdir(CACHDIR)

RESULTDIR = ".result"
if not os.path.exists(RESULTDIR):
    os.mkdir(RESULTDIR)

LOGDIR = ".log"
if not os.path.exists(LOGDIR):
    os.mkdir(LOGDIR)    

def _downloaddata(symbol,duration_seconds,start_dt,end_dt):
    from tqsdk import TqApi,TqAuth,tafunc            
    api = TqApi(auth=TqAuth(tqsdkuser, tqsdkpassword))
    data = api.get_kline_data_series(symbol=symbol, duration_seconds=duration_seconds, start_dt=start_dt,end_dt=end_dt)
    data["datetime"] = data.datetime.apply(lambda x: tafunc.time_to_datetime(x))          
    data["time"] = data['datetime'].dt.time    
    data['date'] = data['datetime'].dt.date
    api.close()            
    return data

def _readdata(filename):
    data = pd.read_csv(filename)     
    data["time"] = data['time'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
    data['date'] = data['date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date())
    return data

def getDataFromTqSdk(symbol : str = "KQ.m@CFFEX.IC",  # 合约代码
                    duration_seconds : int = 60, # 周期
                    csv_filename : str = None, # 缓存文件名
                    start_dt : datetime = datetime(2024, 1, 1), # 开始时间
                    end_dt : date = datetime.now(), # 结束时间
                    reload : bool = False # 是否重新下载
                    ):
    """
    下载数据   默认从csv_filename 取， 如果没有则从tqsdk下载
    """        
    if csv_filename == None or csv_filename == "":
        return _downloaddata(symbol, duration_seconds, start_dt, end_dt)

    filename = os.path.join(CACHDIR, csv_filename)    
    file_exist = os.path.exists(filename) and os.path.getsize(filename) > 0
    if not file_exist or reload:
        data = _downloaddata(symbol, duration_seconds, start_dt, end_dt)        
        data.to_csv(filename, encoding="utf-8", index=False)
    return _readdata(filename)
    
def clearCache(csv_filename : str = "*"):
    """
    清除缓存, "*" 表示清除所有缓存
    """    
    for file in os.listdir(CACHDIR):
        if file == csv_filename or csv_filename == "*":
            os.remove(os.path.join(CACHDIR, file))
    return


if __name__ == "__main__":
    # 测试clearCache
    # 生成一个缓存文件在缓存目录里
    with open(os.path.join(CACHDIR, "test.csv"), "w") as f:
        f.write("test")
    clearCache("test.csv")
    assert not os.path.exists(os.path.join(CACHDIR, "test.csv"))

    # 测试getDataFromTqSdk
    data = getDataFromTqSdk("KQ.m@CFFEX.IH", 60, "test.csv", datetime(2023, 11, 10, 9, 0, 0), datetime(2023, 11, 15, 15,0,0), True)
    assert os.path.exists(os.path.join(CACHDIR, "test.csv"))
    assert len(data) > 0

    # 再次测试getDataFromTqSdk
    data = getDataFromTqSdk("KQ.m@CFFEX.IH", 60, "test.csv", datetime(2023, 11, 10, 9, 0, 0), datetime(2023, 11, 15, 15,0,0), False)
    assert os.path.exists(os.path.join(CACHDIR, "test.csv"))
    assert len(data) > 0



    







    




