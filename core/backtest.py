"""
回测模块
使用backtrader实现回测功能
"""

import backtrader as bt
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
from utils.logger import setup_logger
from config.settings import (
    INITIAL_CAPITAL,
    COMMISSION_RATE
)
from config.indicator_meta import INDICATOR_META

logger = setup_logger(__name__)

class StrategyBase(bt.Strategy):
    """策略基类"""
    params = (
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        """日志记录"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            logger.info(f'{dt.isoformat()} {txt}')

    def notify_order(self, order):
        """订单状态通知"""
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入执行, 价格: {order.executed.price:.2f}, 成本: {order.executed.value:.2f}, 佣金: {order.executed.comm:.2f}')
            else:
                self.log(f'卖出执行, 价格: {order.executed.price:.2f}, 成本: {order.executed.value:.2f}, 佣金: {order.executed.comm:.2f}')

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')

        self.order = None

    def notify_trade(self, trade):
        """交易通知"""
        if not trade.isclosed:
            return

        self.log(f'交易利润, 毛利润: {trade.pnl:.2f}, 净利润: {trade.pnlcomm:.2f}')

class MetaStrategy(StrategyBase):
    """基于INDICATOR_META的通用策略类"""
    
    def __init__(self, strategy_config: Dict[str, Any]):
        """
        初始化策略
        
        Args:
            strategy_config: 策略配置字典，包含name、indicators、params和rule
        """
        super().__init__()
        self.strategy_config = strategy_config
        self.indicators = {}
        
        # 初始化指标
        for indicator in strategy_config['indicators']:
            if indicator in INDICATOR_META:
                meta = INDICATOR_META[indicator]
                params = strategy_config['params'].get(indicator, {})
                
                # 根据指标类型初始化不同的技术指标
                if indicator == 'SMA':
                    period = params.get('period', 20)
                    self.indicators['SMA'] = bt.indicators.SMA(period=period)
                elif indicator == 'EMA':
                    period = params.get('period', 20)
                    self.indicators['EMA'] = bt.indicators.EMA(period=period)
                elif indicator == 'MACD':
                    fast = params.get('fast', 12)
                    slow = params.get('slow', 26)
                    signal = params.get('signal', 9)
                    self.indicators['MACD'] = bt.indicators.MACD(
                        period_me1=fast,
                        period_me2=slow,
                        period_signal=signal
                    )
                elif indicator == 'RSI':
                    period = params.get('period', 14)
                    self.indicators['RSI'] = bt.indicators.RSI(period=period)
                elif indicator == 'Bollinger':
                    period = params.get('period', 20)
                    devfactor = params.get('stdev', 2)
                    self.indicators['Bollinger'] = bt.indicators.BollingerBands(
                        period=period,
                        devfactor=devfactor
                    )
                # 可以添加更多指标...

    def next(self):
        """生成交易信号"""
        if self.order:
            return
            
        # 解析策略规则
        rule = self.strategy_config['rule']
        
        # 根据规则生成信号
        if "close > SMA" in rule:
            if not self.position and self.data.close[0] > self.indicators['SMA'][0]:
                self.buy()
            elif self.position and self.data.close[0] < self.indicators['SMA'][0]:
                self.close()
                
        elif "close < SMA" in rule:
            if not self.position and self.data.close[0] < self.indicators['SMA'][0]:
                self.buy()
            elif self.position and self.data.close[0] > self.indicators['SMA'][0]:
                self.close()
                
        elif "RSI <" in rule:
            th_low = self.strategy_config['params'].get('RSI', {}).get('th_low', 30)
            if not self.position and self.indicators['RSI'][0] < th_low:
                self.buy()
            elif self.position and self.indicators['RSI'][0] > 70:  # 默认超买阈值
                self.close()
                
        elif "RSI >" in rule:
            th_high = self.strategy_config['params'].get('RSI', {}).get('th_high', 70)
            if not self.position and self.indicators['RSI'][0] > th_high:
                self.buy()
            elif self.position and self.indicators['RSI'][0] < 30:  # 默认超卖阈值
                self.close()
                
        # 可以添加更多规则判断...

class BacktestEngine:
    def __init__(self):
        """初始化回测引擎"""
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.setcash(INITIAL_CAPITAL)
        self.cerebro.broker.setcommission(commission=COMMISSION_RATE)
        self.cerebro.addsizer(bt.sizers.PercentSizer, percents=10)  # 每次交易10%仓位
        
        # 添加分析器
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

    def set_data(self, data: pd.DataFrame) -> None:
        """
        设置回测数据
        
        Args:
            data: 包含历史价格和技术指标的DataFrame
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("回测数据必须是pandas DataFrame")
            
        required_columns = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
        if not all(col in data.columns for col in required_columns):
            raise ValueError("回测数据必须包含OHLCV数据")
            
        # 转换数据格式
        data = data.rename(columns={
            'OPEN': 'open',
            'HIGH': 'high',
            'LOW': 'low',
            'CLOSE': 'close',
            'VOLUME': 'volume'
        })
        
        # 添加数据到回测引擎
        datafeed = bt.feeds.PandasData(dataname=data)
        self.cerebro.adddata(datafeed)

    def add_strategy(self, strategy_config: Dict[str, Any]) -> None:
        """
        添加策略
        
        Args:
            strategy_config: 策略配置字典
        """
        self.cerebro.addstrategy(MetaStrategy, strategy_config=strategy_config)

    def run_backtest(self) -> Dict[str, Any]:
        """
        运行回测
        
        Returns:
            Dict[str, Any]: 回测结果
        """
        # 运行回测
        results = self.cerebro.run()
        
        # 获取回测结果
        strat = results[0]
        
        # 计算回测指标
        total_return = (self.cerebro.broker.getvalue() / INITIAL_CAPITAL) - 1
        
        # 计算年化收益率
        days = (strat.data.datetime.date(-1) - strat.data.datetime.date(0)).days
        annual_return = (1 + total_return) ** (365 / days) - 1
        
        # 计算最大回撤
        drawdown = strat.analyzers.drawdown.get_analysis()
        max_drawdown = drawdown['max']['drawdown'] / 100
        
        # 计算夏普比率
        sharpe = strat.analyzers.sharpe.get_analysis()
        sharpe_ratio = sharpe['sharperatio']
        
        # 计算胜率
        trades = strat.analyzers.trades.get_analysis()
        win_rate = trades['won'] / trades['total'] if trades['total'] > 0 else 0
        
        return {
            'strategy_name': strat.strategy_config['name'],
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'total_trades': trades['total'],
            'trades': trades,
            'equity_curve': strat.analyzers.returns.get_analysis()
        }

def backtest_strategy(strategy: Dict[str, Any], 
                     data: pd.DataFrame,
                     initial_capital: float = 100000.0) -> Dict[str, Any]:
    """
    回测单个策略
    
    Args:
        strategy: 策略配置字典
        data: 回测数据
        initial_capital: 初始资金
        
    Returns:
        Dict[str, Any]: 回测结果
    """
    engine = BacktestEngine()
    engine.set_data(data)
    engine.add_strategy(strategy)
    return engine.run_backtest()

def backtest_strategies(strategies: List[Dict[str, Any]],
                       data: pd.DataFrame,
                       initial_capital: float = 100000.0) -> List[Dict[str, Any]]:
    """
    回测多个策略
    
    Args:
        strategies: 策略配置列表
        data: 回测数据
        initial_capital: 初始资金
        
    Returns:
        List[Dict[str, Any]]: 回测结果列表
    """
    results = []
    for strategy in strategies:
        result = backtest_strategy(strategy, data, initial_capital)
        results.append(result)
    return results 