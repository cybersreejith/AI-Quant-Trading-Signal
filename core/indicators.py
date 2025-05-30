import pandas as pd
import numpy as np
import talib
import yfinance as yf
import logging
from datetime import datetime, timedelta
from typing import Optional
from utils.logger import setup_logger
from langchain.agents import tool
logger = setup_logger(__name__)

@tool
def get_historical_data(symbol: str) -> Optional[pd.DataFrame]:
    """
    获取资产的历史数据，默认从当前时间往前推 1 年。    
    参数:
    symbol: 股票代码，如 'AAPL'

    返回:
    包含历史数据的 DataFrame，若失败返回 None
    """
    try:
        # 设置默认日期范围
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            
        # 获取历史数据
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        
        if df.empty:
            logging.warning(f"未找到 {symbol} 的历史数据")
            return None
            
        # 重命名列，只重命名存在的列
        column_mapping = {
            'Open': 'Open',
            'High': 'High',
            'Low': 'Low',
            'Close': 'Close',
            'Volume': 'Volume',
            'Dividends': 'Dividends',
            'Stock Splits': 'Stock_Splits'
        }
        
        # 只重命名存在的列
        existing_columns = [col for col in column_mapping.keys() if col in df.columns]
        df = df.rename(columns={col: column_mapping[col] for col in existing_columns})
        
        return df
        
    except Exception as e:
        logging.error(f"获取 {symbol} 的历史数据时出错: {str(e)}")
        return None

@tool
def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    计算所有技术指标
    :param data: 包含OHLCV数据的DataFrame
    :return: 添加技术指标的DataFrame
    """
    try:
        # 确保数据列名大写
        data.columns = [col.upper() for col in data.columns]
        
        # 计算移动平均线
        data['SMA_5'] = talib.SMA(data['CLOSE'], timeperiod=5)
        data['SMA_10'] = talib.SMA(data['CLOSE'], timeperiod=10)
        data['SMA_20'] = talib.SMA(data['CLOSE'], timeperiod=20)
        data['SMA_50'] = talib.SMA(data['CLOSE'], timeperiod=50)
        data['SMA_200'] = talib.SMA(data['CLOSE'], timeperiod=200)
        
        # 计算指数移动平均线
        data['EMA_5'] = talib.EMA(data['CLOSE'], timeperiod=5)
        data['EMA_10'] = talib.EMA(data['CLOSE'], timeperiod=10)
        data['EMA_20'] = talib.EMA(data['CLOSE'], timeperiod=20)
        data['EMA_50'] = talib.EMA(data['CLOSE'], timeperiod=50)
        
        # 计算MACD
        macd, signal, hist = talib.MACD(data['CLOSE'])
        data['MACD'] = macd
        data['MACD_SIGNAL'] = signal
        data['MACD_HIST'] = hist
        
        # 计算RSI
        data['RSI'] = talib.RSI(data['CLOSE'], timeperiod=14)
        
        # 计算ADX
        data['ADX'] = talib.ADX(data['HIGH'], data['LOW'], data['CLOSE'], timeperiod=14)
        
        # 计算布林带
        upper, middle, lower = talib.BBANDS(data['CLOSE'], timeperiod=20)
        data['BB_UPPER'] = upper
        data['BB_MIDDLE'] = middle
        data['BB_LOWER'] = lower
        
        # 计算ATR
        data['ATR'] = talib.ATR(data['HIGH'], data['LOW'], data['CLOSE'], timeperiod=14)
        
        # 计算唐奇安通道
        data['DONCHIAN_HIGH'] = data['HIGH'].rolling(window=20).max()
        data['DONCHIAN_LOW'] = data['LOW'].rolling(window=20).min()
        
        # 计算ROC
        data['ROC'] = talib.ROC(data['CLOSE'], timeperiod=10)
        
        # 计算成交量指标
        data['OBV'] = talib.OBV(data['CLOSE'], data['VOLUME'])
        
        # 计算随机指标
        slowk, slowd = talib.STOCH(data['HIGH'], data['LOW'], data['CLOSE'])
        data['STOCH_K'] = slowk
        data['STOCH_D'] = slowd
        
        # 计算波动率
        data['VOLATILITY'] = data['CLOSE'].pct_change().rolling(window=20).std() * np.sqrt(252)
        
        # 计算价格变化百分比
        data['PRICE_CHANGE'] = data['CLOSE'].pct_change()
        
        # 计算成交量变化
        data['VOLUME_CHANGE'] = data['VOLUME'].pct_change()
        
        # 计算高低价范围
        data['HIGH_LOW_RANGE'] = (data['HIGH'] - data['LOW']) / data['CLOSE']
        
        # 计算收盘价相对位置
        data['CLOSE_POSITION'] = (data['CLOSE'] - data['BB_LOWER']) / (data['BB_UPPER'] - data['BB_LOWER'])
        
        # 删除包含NaN的行
        data = data.dropna()
        
        logger.info("技术指标计算完成")
        return data
        
    except Exception as e:
        logger.error(f"计算技术指标时出错: {str(e)}")
        return None 