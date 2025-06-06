import pandas as pd
import numpy as np
import talib
import yfinance as yf
import logging
from datetime import datetime, timedelta
from typing import Optional
from utils.logger import setup_logger
logger = setup_logger(__name__)

def get_historical_data(symbol: str) -> Optional[pd.DataFrame]:
    """
    Get historical data for an asset, default from the current time to 1 year ago.    
    Parameters:
    symbol: asset code, e.g. 'AAPL'

    Returns:
    DataFrame containing historical data, or None if failed
    """
    try:
        # Set default date range
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            
        # Get historical data
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        
        if df.empty:
            logging.warning(f"No historical data found for {symbol}")
            return None
            
        # Rename columns, only rename existing columns
        column_mapping = {
            'Open': 'Open',
            'High': 'High',
            'Low': 'Low',
            'Close': 'Close',
            'Volume': 'Volume',
            'Dividends': 'Dividends',
            'Stock Splits': 'Stock_Splits'
        }
        
        # Only rename existing columns
        existing_columns = [col for col in column_mapping.keys() if col in df.columns]
        df = df.rename(columns={col: column_mapping[col] for col in existing_columns})
        
        return df
        
    except Exception as e:
        logging.error(f"Error getting historical data for {symbol}: {str(e)}")
        return None

def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate all technical indicators
    :param data: DataFrame containing OHLCV data
    :return: DataFrame with added technical indicators
    """
    try:
        # Ensure data column names are uppercase
        data.columns = [col.upper() for col in data.columns]
        
        # Calculate moving average lines
        data['SMA_5'] = talib.SMA(data['CLOSE'], timeperiod=5)
        data['SMA_10'] = talib.SMA(data['CLOSE'], timeperiod=10)
        data['SMA_20'] = talib.SMA(data['CLOSE'], timeperiod=20)
        data['SMA_50'] = talib.SMA(data['CLOSE'], timeperiod=50)
        data['SMA_200'] = talib.SMA(data['CLOSE'], timeperiod=200)
        
        # Calculate exponential moving average lines
        data['EMA_5'] = talib.EMA(data['CLOSE'], timeperiod=5)
        data['EMA_10'] = talib.EMA(data['CLOSE'], timeperiod=10)
        data['EMA_20'] = talib.EMA(data['CLOSE'], timeperiod=20)
        data['EMA_50'] = talib.EMA(data['CLOSE'], timeperiod=50)
        
        # Calculate MACD
        macd, signal, hist = talib.MACD(data['CLOSE'])
        data['MACD'] = macd
        data['MACD_SIGNAL'] = signal
        data['MACD_HIST'] = hist
        
        # Calculate RSI
        data['RSI'] = talib.RSI(data['CLOSE'], timeperiod=14)
        
        # Calculate ADX
        data['ADX'] = talib.ADX(data['HIGH'], data['LOW'], data['CLOSE'], timeperiod=14)
        
        # Calculate Bollinger Bands
        upper, middle, lower = talib.BBANDS(data['CLOSE'], timeperiod=20)
        data['BB_UPPER'] = upper
        data['BB_MIDDLE'] = middle
        data['BB_LOWER'] = lower
        
        # Calculate ATR
        data['ATR'] = talib.ATR(data['HIGH'], data['LOW'], data['CLOSE'], timeperiod=14)
        
        # Calculate Donchian Channels
        data['DONCHIAN_HIGH'] = data['HIGH'].rolling(window=20).max()
        data['DONCHIAN_LOW'] = data['LOW'].rolling(window=20).min()
        
        # Calculate ROC
        data['ROC'] = talib.ROC(data['CLOSE'], timeperiod=10)
        
        # Calculate volume indicators
        data['OBV'] = talib.OBV(data['CLOSE'], data['VOLUME'])
        
        # Calculate stochastic indicators
        slowk, slowd = talib.STOCH(data['HIGH'], data['LOW'], data['CLOSE'])
        data['STOCH_K'] = slowk
        data['STOCH_D'] = slowd
        
        # Calculate volatility
        data['VOLATILITY'] = data['CLOSE'].pct_change().rolling(window=20).std() * np.sqrt(252)
        
        # Calculate price change percentage
        data['PRICE_CHANGE'] = data['CLOSE'].pct_change()
        
        # Calculate volume change
        data['VOLUME_CHANGE'] = data['VOLUME'].pct_change()
        
        # Calculate high-low range
        data['HIGH_LOW_RANGE'] = (data['HIGH'] - data['LOW']) / data['CLOSE']
        
        # Calculate closing price relative position
        data['CLOSE_POSITION'] = (data['CLOSE'] - data['BB_LOWER']) / (data['BB_UPPER'] - data['BB_LOWER'])
        
        # Drop rows containing NaN
        data = data.dropna()
        
        logger.info("Technical indicators calculated")
        return data
        
    except Exception as e:
        logger.error(f"Error calculating technical indicators: {str(e)}")
        return None 