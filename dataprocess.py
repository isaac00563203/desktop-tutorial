import talib

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
                    'RSI': ['RSI6', 'RSI12', 'RSI24'],
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
    
def add_tech_index(df, tech_list, tech_para_list):
    for tech in tech_list:
        if tech in tech_para_list.keys():
            para = tech_para_list[tech]
            colunm_name = tech_name_list[tech]
            if len(colunm_name) < len(para):
                print('列名与参数个数不匹配')
                return None
            
            # 如果参数为空，则直接计算
            if len(para) == 0:
                print('无参数技术指标：', tech)
                result = tech_index(df, tech, para)
                if isinstance(result, tuple):
                    for i in range(len(result)):
                        df[colunm_name[i]] = result[i]
                else:
                    df[colunm_name[0]] = result
                        
            elif isinstance(para[0], list) == False:
                print('单参数技术指标：', tech)
                for i in range(len(para)):
                    result = tech_index(df, tech, para[i])
                    # 如果返回值是元组，则需要分别赋值
                    if isinstance(result, tuple):
                        for j in range(len(result)):
                            df[colunm_name[i][j]] = result[j]
                    else:
                        df[colunm_name[i]] = result
            else:
                print('多参数技术指标：', tech)
                for i in range(len(para)):
                    result = tech_index(df, tech, para[i])
                    if isinstance(result, tuple):
                        for j in range(len(result)):
                            df[colunm_name[i][j]] = result[j]
                    else:
                        print('多参数技术指标返回值错误')                
    return df
        
if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(np.random.randn(100, 5), columns=['open', 'high', 'low', 'close', 'volume'])
    df = add_tech_index(df, tech_list, tech_para_list)
    print(df.tail(10))
    print(df.columns)