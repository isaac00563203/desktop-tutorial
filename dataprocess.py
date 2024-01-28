import talib
from pandas import DataFrame
from datetime import time
from sklearn.preprocessing import StandardScaler

# 技术指标列表
tech_list = ['MA', 'EMA', 'MACD', 'KDJ', 'RSI', 'BOLL', 'SAR', 'CCI', 'ATR', 'OBV', 'WILLR', 'AD']

# 技术指标参数列表
tech_para_list = {'MA': [5, 10, 20, 30, 60, 120, 250],
                  'EMA': [5, 10, 20, 30, 60, 120, 250],
                  'MACD': [[12, 26, 9]],
                  'KDJ': [[9, 3, 3]],
                  'RSI': [[6, 12, 24]],
                  'BOLL': [[26, 2]],
                  'SAR': [[0.02, 0.2]],
                  'CCI': [14],
                  'ATR': [14],
                  'OBV': [],
                  'WILLR': [14],
                  'AD': []
}

# 技术指标函数列表
tech_func_list = {'MA': talib.MA,
                  'EMA': talib.EMA,
                  'MACD': talib.MACD,
                  'KDJ': talib.STOCH,
                  'RSI': talib.RSI,
                  'BOLL': talib.BBANDS,
                  'SAR': talib.SAR,
                  'CCI': talib.CCI,
                  'ATR': talib.ATR,
                  'OBV': talib.OBV,
                  'WILLR': talib.WILLR,
                  'AD': talib.AD
}

# 技术指标名称列表
tech_name_list = {'MA': ['MA5', 'MA10', 'MA20', 'MA30', 'MA60', 'MA120', 'MA250'],
                    'EMA': ['EMA5', 'EMA10', 'EMA20', 'EMA30', 'EMA60', 'EMA120', 'EMA250'],
                    'MACD': [['DIFF', 'DEA', 'MACD']],
                    'KDJ': [['KDJ_K', 'KDJ_D']],  # KDJ返回值是元组 只返回KD两个值
                    'RSI': [['RSI6', 'RSI12', 'RSI24']],
                    'BOLL': [['BOLL_UPPER', 'BOLL_MIDDLE', 'BOLL_LOWER']],
                    'SAR': ['SAR'],
                    'CCI': ['CCI'],
                    'ATR': ['ATR'],
                    'OBV': ['OBV'],
                    'WILLR': ['WILLR'],
                    'AD': ['AD']
}

# 定义技术指标函数
def tech_index(df, tech, para):
    if tech == 'MA':
        return tech_func_list[tech](df['close'], para)
    elif tech == 'EMA':
        return tech_func_list[tech](df['close'], para)
    elif tech == 'MACD':
        return tech_func_list[tech](df['close'], para[0], para[1], para[2])
    elif tech == 'KDJ':
        return tech_func_list[tech](df['high'], df['low'], df['close'], para[0], para[1], para[2])
    elif tech == 'RSI':
        return tech_func_list[tech](df['close'], para[0]), tech_func_list[tech](df['close'], para[1]), tech_func_list[tech](df['close'], para[2])
    elif tech == 'BOLL':
        return tech_func_list[tech](df['close'], para[0], para[1])
    elif tech == 'SAR':
        return tech_func_list[tech](df['high'], df['low'], para[0], para[1])
    elif tech == 'CCI':
        return tech_func_list[tech](df['high'], df['low'], df['close'], para)
    elif tech == 'ATR':
        return tech_func_list[tech](df['high'], df['low'], df['close'], para)
    elif tech == 'OBV':
        return tech_func_list[tech](df['close'], df['volume'])
    elif tech == 'WILLR':
        return tech_func_list[tech](df['high'], df['low'], df['close'], para)
    elif tech == 'AD':
        return tech_func_list[tech](df['high'], df['low'], df['close'], df['volume'])
    else:
        return None 
    
def add_tech_index(df : DataFrame, tech_list : list, tech_para_list : dict):
    """
    为df增加技术指标,并返回df    
    df : DataFrame
    tech_list : 技术指标列表
    tech_para_list : 技术指标参数列表
    注意:
        1. tech_list 与 tech_para_list 的长度必须一致
        2. tech_para_list 中的参数个数必须与 tech_name_list 中的列名个数一致        
    """
    for tech in tech_list:
        if tech in tech_para_list.keys():
            para = tech_para_list[tech]
            colunm_name = tech_name_list[tech]
            if len(colunm_name) < len(para):
                print('列名与参数个数不匹配')
                return None
            
            # 如果参数为空，则直接计算
            if len(para) == 0:                
                result = tech_index(df, tech, para)
                if isinstance(result, tuple):
                    for i in range(len(result)):
                        df[colunm_name[i]] = result[i]
                else:
                    df[colunm_name[0]] = result
                        
            elif isinstance(para[0], list) == False:                
                for i in range(len(para)):
                    result = tech_index(df, tech, para[i])
                    # 如果返回值是元组，则需要分别赋值
                    if isinstance(result, tuple):
                        for j in range(len(result)):
                            df[colunm_name[i][j]] = result[j]
                    else:
                        df[colunm_name[i]] = result
            else:                
                for i in range(len(para)):
                    result = tech_index(df, tech, para[i])
                    if isinstance(result, tuple):
                        for j in range(len(result)):                            
                            df[colunm_name[i][j]] = result[j]
                    else:
                        df[colunm_name[i]] = result                                    
    return df
        
# 标准化数据 
# 标准化后的数据存放在 "n_" 开头的列中
def standardscaler_data(data : DataFrame,
            tech_list : list = ["open", "high", "low", "close", "volume"]
            ) -> DataFrame:        
    fun = StandardScaler()
    for tech in tech_list:
        if tech in data.columns:
            n_tech = "n_" + tech
            data[n_tech] = fun.fit_transform(data[tech].values.reshape(-1, 1))
    return data

# 取出所有的技术指标名称
def get_tech_name_list(tech_list):        
    tech_name_list = []
    for tech in tech_list:
        if tech in tech_name_list.keys():
            colunm_name = tech_name_list[tech]
            if isinstance(colunm_name[0], list):
                for i in range(len(colunm_name)):
                    tech_name_list.extend(colunm_name[i])
            else:
                tech_name_list.extend(colunm_name)
    return tech_name_list


# 预处理数据
def pre_cook_data(df : DataFrame,
                  tech_list : list = tech_list,
                  tech_para_list : dict = tech_para_list,                  
                  origindata : bool = True
                  ) -> DataFrame:
    # 计算技术指标
    df = add_tech_index(df, tech_list, tech_para_list)
    # 取出所有的技术指标名称
    use_tech_name_list = get_tech_name_list(tech_list)

    if origindata:
        if "close" not in use_tech_name_list:
            use_tech_name_list.append("close")
        if "high" not in use_tech_name_list:
            use_tech_name_list.append("high")
        if "low" not in use_tech_name_list:
            use_tech_name_list.append("low")
        if "open" not in use_tech_name_list:
            use_tech_name_list.append("open")    
        if "volume" not in use_tech_name_list:
            use_tech_name_list.append("volume")         

    # 为每日数据增加序列号
    df["minute_index"] = df.groupby("date").cumcount()
    use_tech_name_list.append("minute_index")

    print(f"技术指标列表: {use_tech_name_list}")
    # 数据正则化
    df = standardscaler_data(df, use_tech_name_list)
    # 去掉前240行
    df = df.iloc[240:]
    
    return df

if __name__ == "__main__":
    import pandas as pd
    import numpy as np    
    from datetime import datetime
    
    df = pd.read_csv(".cache/test.csv")
    df["datetime"] = df.datetime.apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))        
    df["time"] = df['time'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
    df['date'] = df['date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date())
    
    # 计算技术指标
    df = add_tech_index(df, tech_list, tech_para_list)

    df = pre_cook_data(df, tech_list, tech_para_list, tech_name_list)

    #为每日数据增加序列号
    df["date_index"] = df.groupby("date").cumcount()
    print(df.columns)
    print(df.head())
    print(df.tail())
    


    # 计算时间戳
    # timestamp = df["datetime"].apply(lambda x: x.timestamp())
    # min_time = timestamp.min()
    # df["timeline"] = timestamp - min_time
    # print(df.columns)
    # print(df.head())
    
    


