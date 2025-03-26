import yfinance as yf
from typing import Optional
import pandas as pd
from datetime import datetime
from config.settings import DEFAULT_TIMEFRAME, DEFAULT_START_DATE, DEFAULT_END_DATE
from utils.logger import setup_logger

logger = setup_logger(__name__)

def get_asset_data(symbol: str, start_date: str = None, end_date: str = None) -> Optional[pd.DataFrame]:
    """
    获取资产数据
    :param symbol: 资产代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 包含OHLCV数据的DataFrame
    """
    try:
        # 使用默认日期
        start_date = start_date or DEFAULT_START_DATE
        end_date = end_date or DEFAULT_END_DATE
        
        # 获取数据
        ticker = yf.Ticker(symbol)
        df = ticker.history(
            start=start_date,
            end=end_date,
            interval=DEFAULT_TIMEFRAME
        )
        
        if df.empty:
            logger.error(f"无法获取资产 {symbol} 的数据")
            return None
            
        # 重命名列
        df.columns = [col.upper() for col in df.columns]
        
        # 设置索引名称
        df.index.name = symbol
        
        logger.info(f"成功获取资产 {symbol} 的数据，共 {len(df)} 条记录")
        return df
        
    except Exception as e:
        logger.error(f"获取资产 {symbol} 数据时出错: {str(e)}")
        return None

def identify_asset_type(symbol: str) -> str:
    """
    识别资产类型
    :param symbol: 资产代码
    :return: 资产类型
    """
    if symbol.startswith('^'):
        return "指数"
    elif symbol.endswith('-USD'):
        return "加密货币"
    elif symbol.endswith('=X'):
        return "外汇"
    elif symbol.endswith('=F'):
        return "期货"
    else:
        return "股票" 