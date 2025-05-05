import pandas as pd
import numpy as np
import yfinance as yf
import talib
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import os
from utils.logger import setup_logger
from core.indicators import calculate_indicators
from core.backtest import Backtest
from config.settings import (
    START_DATE,
    END_DATE,
    EMAIL_RECIPIENTS,
    EMAIL_SUBJECT,
    POPULAR_ASSETS
)

logger = setup_logger(__name__)

# 资产类型定义
ASSET_TYPES = {
    '1': {'name': '全球股票', 'suffix': ''},
    '2': {'name': 'ETF', 'suffix': '.ETF'},
    '3': {'name': '外汇', 'suffix': '=X'},
    '4': {'name': '加密货币', 'suffix': '-USD'}
}





def select_asset_type_menu() -> Optional[str]:
    """
    显示资产类型菜单并获取用户选择
    
    Returns:
        用户选择的资产类型代码，如果选择退出则返回None
    """
    print("\n=== AI量化交易分析系统 ===")
    print("1. 全球股票")
    print("2. ETF")
    print("3. 外汇")
    print("4. 加密货币")
    print("5. 退出")
    
    while True:
        choice = input("\n请选择资产类型 (1-5): ")
        
        if choice == '5':
            return None
            
        if choice in ['1', '2', '3', '4']:
            return choice
            
        print("无效的选择，请重试")

def input_asset_symbol() -> Optional[str]:
    """
    获取用户输入的资产代码
    
    Returns:
        用户输入的资产代码，如果输入为空则返回None
    """
    symbol = input("\n请输入要分析的资产代码: ").strip()
    if not symbol:
        print("未输入资产代码")
        return None
    return symbol





def get_historical_data(symbol: str, start_date: str = None, end_date: str = None) -> Optional[pd.DataFrame]:
    """
    获取历史数据
    
    Args:
        symbol: 资产代码
        start_date: 开始日期，格式：'YYYY-MM-DD'
        end_date: 结束日期，格式：'YYYY-MM-DD'
        
    Returns:
        包含历史数据的DataFrame，如果获取失败则返回None
    """
    try:
        # 设置默认日期范围
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
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

def prepare_backtest_data(symbols: List[str], start_date: str = None, end_date: str = None) -> Dict[str, pd.DataFrame]:
    """
    准备回测数据
    
    Args:
        symbols: 资产代码列表
        start_date: 开始日期
        end_date: 结束日期
        
    Returns:
        包含每个资产数据的字典
    """
    try:
        datasets = {}
        
        for symbol in symbols:
            # 获取历史数据
            historical_data = get_historical_data(symbol, start_date, end_date)
            if historical_data is None:
                continue
                
            # 计算技术指标
            technical_data = calculate_indicators(historical_data)
            if technical_data is None:
                continue
                
            # 保存到结果字典
            datasets[symbol] = technical_data
            
        return datasets
        
    except Exception as e:
        logging.error(f"准备回测数据时出错: {str(e)}")
        return {}




def display_asset_reference_list(asset_type: str) -> None:
    """
    显示资产参考列表
    
    Args:
        asset_type: 资产类型代码
    """
    print(f"\n=== {POPULAR_ASSETS[asset_type]['name']} 参考列表 ===")
    for i, asset in enumerate(POPULAR_ASSETS[asset_type]['assets'], 1):
        print(f"{i}. {asset}")

def get_date_range() -> tuple[str, str]:
    """
    获取过去一年的日期范围
    
    Returns:
        开始日期和结束日期的元组 (YYYY-MM-DD格式)
    """
    # 计算日期范围（过去一年）
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    logger.info(f"使用时间范围: {start_date} 至 {end_date}")
    return start_date, end_date

def run_trading_analysis() -> None:
    """
    运行交易分析主程序
    """
    try:
        while True:
            # 选择资产类型
            choice = select_asset_type_menu()
            if choice is None:
                break
                
            # 显示参考列表
            display_asset_reference_list(choice)
                
            # 输入资产代码
            symbol = input_asset_symbol()
            if symbol is None:
                continue
                
            print(f"\n已选择资产: {symbol}")
            
            # 获取日期范围
            start_date, end_date = get_date_range()
            
            # 获取历史数据
            historical_data = get_historical_data(symbol, start_date, end_date)
            if historical_data is None:
                print("获取历史数据失败")
                continue
                
            # 计算技术指标
            technical_data = calculate_indicators(historical_data)
            if technical_data is None:
                print("计算技术指标失败")
                continue
                

            
    except Exception as e:
        logging.error(f"运行交易分析时出错: {str(e)}")
        raise

if __name__ == "__main__":
    run_trading_analysis() 