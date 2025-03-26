import pandas as pd
import numpy as np
import talib
from utils.logger import setup_logger

logger = setup_logger(__name__)

def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    计算技术指标
    :param data: 包含OHLCV数据的DataFrame
    :return: 添加技术指标的DataFrame
    """
    try:
        # 确保数据列名大写
        data.columns = [col.upper() for col in data.columns]
        
        # 计算移动平均线
        data['SMA20'] = talib.SMA(data['CLOSE'], timeperiod=20)
        data['SMA50'] = talib.SMA(data['CLOSE'], timeperiod=50)
        data['SMA200'] = talib.SMA(data['CLOSE'], timeperiod=200)
        data['EMA5'] = talib.EMA(data['CLOSE'], timeperiod=5)
        data['EMA20'] = talib.EMA(data['CLOSE'], timeperiod=20)
        
        # 计算MACD
        macd, signal, hist = talib.MACD(data['CLOSE'])
        data['MACD'] = macd
        data['SIGNAL'] = signal
        data['MACD_HIST'] = hist
        
        # 计算RSI
        data['RSI'] = talib.RSI(data['CLOSE'], timeperiod=14)
        
        # 计算ADX
        data['ADX'] = talib.ADX(data['HIGH'], data['LOW'], data['CLOSE'], timeperiod=14)
        
        # 计算布林带
        upper, middle, lower = talib.BBANDS(data['CLOSE'], timeperiod=20)
        data['UPPER'] = upper
        data['MIDDLE'] = middle
        data['LOWER'] = lower
        
        # 计算ATR
        data['ATR'] = talib.ATR(data['HIGH'], data['LOW'], data['CLOSE'], timeperiod=14)
        
        # 计算唐奇安通道
        data['DONCHIAN_HIGH'] = data['HIGH'].rolling(window=20).max()
        data['DONCHIAN_LOW'] = data['LOW'].rolling(window=20).min()
        
        # 计算ROC
        data['ROC'] = talib.ROC(data['CLOSE'], timeperiod=10)
        
        logger.info("技术指标计算完成")
        return data
        
    except Exception as e:
        logger.error(f"计算技术指标时出错: {str(e)}")
        return None 