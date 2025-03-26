import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from utils.logger import setup_logger
from config.settings import (
    RSI_OVERSOLD,
    RSI_OVERBOUGHT,
    MACD_SIGNAL_PERIOD,
    MACD_FAST_PERIOD,
    MACD_SLOW_PERIOD,
    ADX_THRESHOLD,
    ATR_MULTIPLIER
)

logger = setup_logger(__name__)

class TunableClassicTrendFollow:
    """
    可调参数的经典趋势跟踪策略
    """
    def __init__(self):
        self.position = 0  # 1: 多头, -1: 空头, 0: 空仓
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        
    def analyze_single_asset(self, data: pd.DataFrame, sentiment_score: float = 0) -> Dict:
        """
        分析单个资产的交易信号
        :param data: 包含价格和技术指标数据的DataFrame
        :param sentiment_score: 市场情绪得分 (-1 到 1)
        :return: 交易信号字典
        """
        try:
            latest = data.iloc[-1]
            prev = data.iloc[-2]
            
            # 计算趋势强度
            trend_strength = self._calculate_trend_strength(latest)
            
            # 计算动量指标
            momentum = self._calculate_momentum(latest, prev)
            
            # 计算波动率
            volatility = self._calculate_volatility(latest)
            
            # 生成交易信号
            signal = self._generate_signal(
                latest,
                trend_strength,
                momentum,
                volatility,
                sentiment_score
            )
            
            if signal is None:
                return None
            
            # 计算止损和止盈价格
            stop_loss, take_profit = self._calculate_exit_prices(
                latest['CLOSE'],
                volatility,
                signal['direction']
            )
            
            return {
                'symbol': data.name,
                'timestamp': pd.Timestamp.now(),
                'signal': signal['direction'],
                'strength': signal['strength'],
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'reasoning': signal['reasoning'],
                'timestamp': pd.Timestamp.now()
            }
            
        except Exception as e:
            logger.error(f"分析交易信号时出错: {str(e)}")
            return None
            
    def _calculate_trend_strength(self, data: pd.DataFrame) -> float:
        """
        计算趋势强度
        :param data: 当前数据点
        :return: 趋势强度得分 (-1 到 1)
        """
        # 使用ADX判断趋势强度
        adx = data['ADX']
        if adx < ADX_THRESHOLD:
            return 0
            
        # 使用均线系统判断趋势方向
        if data['SMA20'] > data['SMA50'] > data['SMA200']:
            return min(1.0, adx / 100)
        elif data['SMA20'] < data['SMA50'] < data['SMA200']:
            return max(-1.0, -adx / 100)
        return 0
        
    def _calculate_momentum(self, latest: pd.DataFrame, prev: pd.DataFrame) -> float:
        """
        计算动量
        :param latest: 最新数据点
        :param prev: 前一个数据点
        :return: 动量得分 (-1 到 1)
        """
        # RSI动量
        rsi_momentum = (latest['RSI'].iloc[-1] - prev['RSI'].iloc[-1]) / 100
        
        # MACD动量
        macd_momentum = (latest['MACD'].iloc[-1] - prev['MACD'].iloc[-1]) / abs(prev['MACD'].iloc[-1]) if prev['MACD'].iloc[-1] != 0 else 0
        
        # 价格动量
        price_momentum = (latest['CLOSE'].iloc[-1] - prev['CLOSE'].iloc[-1]) / prev['CLOSE'].iloc[-1]
        
        # 综合动量得分
        return (rsi_momentum + macd_momentum + price_momentum) / 3
        
    def _calculate_volatility(self, data: pd.DataFrame) -> float:
        """
        计算波动率
        :param data: 当前数据点
        :return: 波动率
        """
        return data['ATR'].iloc[-1] / data['CLOSE'].iloc[-1]
        
    def _generate_signal(self, latest: pd.DataFrame, trend_strength: float, momentum: float, volatility: float, sentiment_score: float) -> Dict:
        """
        生成交易信号
        :param latest: 最新数据点
        :param trend_strength: 趋势强度
        :param momentum: 动量
        :param volatility: 波动率
        :param sentiment_score: 市场情绪得分
        :return: 交易信号字典
        """
        # 计算综合得分
        technical_score = (trend_strength + momentum) / 2
        total_score = (technical_score + sentiment_score) / 2
        
        # 生成信号
        if total_score > 0.6:  # 强买入信号
            return {
                'direction': 1,
                'strength': 'strong',
                'reasoning': f"强买入信号: 趋势强度={trend_strength:.2f}, 动量={momentum:.2f}, 情绪={sentiment_score:.2f}"
            }
        elif total_score > 0.3:  # 弱买入信号
            return {
                'direction': 1,
                'strength': 'weak',
                'reasoning': f"弱买入信号: 趋势强度={trend_strength:.2f}, 动量={momentum:.2f}, 情绪={sentiment_score:.2f}"
            }
        elif total_score < -0.6:  # 强卖出信号
            return {
                'direction': -1,
                'strength': 'strong',
                'reasoning': f"强卖出信号: 趋势强度={trend_strength:.2f}, 动量={momentum:.2f}, 情绪={sentiment_score:.2f}"
            }
        elif total_score < -0.3:  # 弱卖出信号
            return {
                'direction': -1,
                'strength': 'weak',
                'reasoning': f"弱卖出信号: 趋势强度={trend_strength:.2f}, 动量={momentum:.2f}, 情绪={sentiment_score:.2f}"
            }
        else:  # 无信号
            return {
                'direction': 0,
                'strength': 'neutral',
                'reasoning': f"无信号: 趋势强度={trend_strength:.2f}, 动量={momentum:.2f}, 情绪={sentiment_score:.2f}"
            }
            
    def _calculate_exit_prices(self, close: float, volatility: float, direction: int) -> Tuple[float, float]:
        """
        计算止损和止盈价格
        :param close: 最新收盘价
        :param volatility: 波动率
        :param direction: 交易方向
        :return: (止损价格, 止盈价格)
        """
        atr = close * volatility
        if direction > 0:  # 多头
            stop_loss = close - (atr * ATR_MULTIPLIER)
            take_profit = close + (atr * ATR_MULTIPLIER * 2)
        elif direction < 0:  # 空头
            stop_loss = close + (atr * ATR_MULTIPLIER)
            take_profit = close - (atr * ATR_MULTIPLIER * 2)
        else:  # 无方向
            stop_loss = take_profit = close
            
        return stop_loss, take_profit 