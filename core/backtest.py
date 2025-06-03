"""
回测模块
使用backtrader实现回测功能
"""

import backtrader as bt
from langchain.agents import tool
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Union
from datetime import datetime
from utils.logger import setup_logger
from config.settings import (
    INITIAL_CAPITAL,
    COMMISSION_RATE
)
import json

logger = setup_logger(__name__)

class BacktestEngine:
    def __init__(self):
        """初始化回测引擎"""
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.setcash(INITIAL_CAPITAL)
        self.cerebro.broker.setcommission(commission=COMMISSION_RATE)
        self.cerebro.addsizer(bt.sizers.PercentSizer, percents=10)  # 每次交易10%仓位
        self.strategy_config = None
        
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
            strategy_config: 策略配置字典，由generate_strategies生成
        """
        self.strategy_config = strategy_config
        
        # 创建策略类
        class Strategy(bt.Strategy):
            def __init__(self):
                self.indicators = {}
                for indicator in strategy_config['indicators']:
                    params = strategy_config['params'].get(indicator, {})
                    self.indicators[indicator] = getattr(bt.indicators, indicator)(**params)
                    
            def next(self):
                if self.order:
                    return
                    
                rule = strategy_config['rule']
                if not self.position:
                    if eval(rule, {
                        'close': self.data.close[0],
                        **{k: v[0] for k, v in self.indicators.items()}
                    }):
                        self.buy()
                else:
                    if not eval(rule, {
                        'close': self.data.close[0],
                        **{k: v[0] for k, v in self.indicators.items()}
                    }):
                        self.close()
                        
        self.cerebro.addstrategy(Strategy)

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
            'strategy_name': self.strategy_config['name'],
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'total_trades': trades['total'],
            'trades': trades,
            'equity_curve': strat.analyzers.returns.get_analysis()
        }


@tool("回测交易策略")
def backtest_strategy(data: pd.DataFrame,
                       strategy: Dict[str, Any],
                       initial_capital: float = 100000.0) -> Dict[str, Any]:
    """
    回测单个交易策略
    
    Args:
        data: 回测数据
        strategy: 策略配置字典
        initial_capital: 初始资金
        
    Returns:
        Dict[str, Any]: 回测结果
    """
    engine = BacktestEngine()
    engine.set_data(data)
    engine.add_strategy(strategy)
    return engine.run_backtest()

@tool("评估策略回测结果并生成性能分析报告")
def evaluate_backtest(backtest_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    评估回测效果，生成详细的性能分析报告
    
    Args:
        backtest_results: 回测结果字典，包含策略名称、收益率、回撤等信息
        
    Returns:
        Dict[str, Any]: 包含详细评估指标的字典
    """
    # 基础指标
    total_return = backtest_results['total_return']
    annual_return = backtest_results['annual_return']
    max_drawdown = backtest_results['max_drawdown']
    sharpe_ratio = backtest_results['sharpe_ratio']
    win_rate = backtest_results['win_rate']
    total_trades = backtest_results['total_trades']
    
    # 计算风险调整后的收益指标
    sortino_ratio = annual_return / (max_drawdown + 1e-6)  # 索提诺比率
    calmar_ratio = annual_return / (max_drawdown + 1e-6)   # 卡玛比率
    
    # 交易统计
    trades = backtest_results['trades']
    avg_trade_return = trades['pnl']['net']['average'] if 'pnl' in trades else 0
    profit_factor = trades['pnl']['net']['total'] / abs(trades['pnl']['net']['total'] - trades['pnl']['gross']['total']) if 'pnl' in trades else 0
    
    # 资金曲线分析
    equity_curve = backtest_results['equity_curve']
    equity_series = pd.Series(equity_curve)
    volatility = equity_series.pct_change().std() * np.sqrt(252)  # 年化波动率
    
    # 计算连续亏损次数
    consecutive_losses = 0
    max_consecutive_losses = 0
    for trade in trades.get('trades', []):
        if trade['pnl'] < 0:
            consecutive_losses += 1
            max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
        else:
            consecutive_losses = 0
    
    # 生成评估报告
    evaluation_report = {
        'strategy_name': backtest_results['strategy_name'],
        'performance_metrics': {
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'calmar_ratio': calmar_ratio,
            'volatility': volatility
        },
        'trading_statistics': {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'avg_trade_return': avg_trade_return,
            'max_consecutive_losses': max_consecutive_losses
        },
        'risk_metrics': {
            'value_at_risk_95': equity_series.pct_change().quantile(0.05),
            'expected_shortfall': equity_series.pct_change()[equity_series.pct_change() <= equity_series.pct_change().quantile(0.05)].mean()
        }
    }
    
    # 添加评估结论
    evaluation_report['conclusion'] = {
        'overall_rating': '优秀' if (sharpe_ratio > 1.5 and win_rate > 0.6 and max_drawdown < 0.2) else 
                         '良好' if (sharpe_ratio > 1.0 and win_rate > 0.5 and max_drawdown < 0.3) else 
                         '一般' if (sharpe_ratio > 0.5 and win_rate > 0.4 and max_drawdown < 0.4) else '较差',
        'strengths': [],
        'weaknesses': []
    }
    
    # 分析优势和劣势
    if sharpe_ratio > 1.0:
        evaluation_report['conclusion']['strengths'].append('风险调整后收益表现优秀')
    if win_rate > 0.6:
        evaluation_report['conclusion']['strengths'].append('胜率较高')
    if max_drawdown < 0.2:
        evaluation_report['conclusion']['strengths'].append('回撤控制良好')
        
    if sharpe_ratio < 0.5:
        evaluation_report['conclusion']['weaknesses'].append('风险调整后收益表现不佳')
    if win_rate < 0.4:
        evaluation_report['conclusion']['weaknesses'].append('胜率较低')
    if max_drawdown > 0.3:
        evaluation_report['conclusion']['weaknesses'].append('回撤较大')
    
    return evaluation_report