import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from utils.logger import setup_logger
from config.settings import (
    INITIAL_CAPITAL,
    POSITION_SIZE,
    COMMISSION_RATE,
    SLIPPAGE
)

logger = setup_logger(__name__)

class Backtest:
    """
    回测系统
    """
    def __init__(self, initial_capital: float = INITIAL_CAPITAL):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {}  # 当前持仓
        self.trades = []  # 交易记录
        self.equity_curve = []  # 权益曲线
        
    def run(self, data: pd.DataFrame, signals: List[Dict]) -> Dict:
        """
        运行回测
        :param data: 历史数据
        :param signals: 交易信号列表
        :return: 回测结果
        """
        try:
            for i in range(len(data)):
                current_price = data.iloc[i]['CLOSE']
                timestamp = data.index[i]
                
                # 更新持仓盈亏
                self._update_positions(current_price, timestamp)
                
                # 处理交易信号
                for signal in signals:
                    if signal['timestamp'] == timestamp:
                        self._process_signal(signal, current_price)
                
                # 记录权益
                self.equity_curve.append({
                    'timestamp': timestamp,
                    'equity': self._calculate_total_equity(current_price)
                })
            
            # 计算回测结果
            results = self._calculate_results()
            logger.info("回测完成")
            return results
            
        except Exception as e:
            logger.error(f"回测过程中出错: {str(e)}")
            return None
            
    def _update_positions(self, current_price: float, timestamp: pd.Timestamp):
        """
        更新持仓盈亏
        :param current_price: 当前价格
        :param timestamp: 时间戳
        """
        for symbol, position in self.positions.items():
            # 计算未实现盈亏
            unrealized_pnl = position['size'] * (current_price - position['entry_price'])
            
            # 检查止损止盈
            if position['direction'] > 0:  # 多头
                if current_price <= position['stop_loss']:
                    self._close_position(symbol, current_price, timestamp, 'stop_loss')
                elif current_price >= position['take_profit']:
                    self._close_position(symbol, current_price, timestamp, 'take_profit')
            else:  # 空头
                if current_price >= position['stop_loss']:
                    self._close_position(symbol, current_price, timestamp, 'stop_loss')
                elif current_price <= position['take_profit']:
                    self._close_position(symbol, current_price, timestamp, 'take_profit')
                    
    def _process_signal(self, signal: Dict, current_price: float):
        """
        处理交易信号
        :param signal: 交易信号
        :param current_price: 当前价格
        """
        symbol = signal['symbol']
        
        # 如果已有持仓，先平仓
        if symbol in self.positions:
            self._close_position(symbol, current_price, signal['timestamp'], 'signal')
        
        # 开新仓
        if signal['direction'] != 0:
            self._open_position(signal, current_price)
            
    def _open_position(self, signal: Dict, current_price: float):
        """
        开仓
        :param signal: 交易信号
        :param current_price: 当前价格
        """
        symbol = signal['symbol']
        direction = signal['direction']
        size = POSITION_SIZE * self.initial_capital / current_price
        
        # 计算交易成本
        commission = size * current_price * COMMISSION_RATE
        slippage = size * current_price * SLIPPAGE
        total_cost = commission + slippage
        
        # 检查资金是否足够
        if total_cost > self.current_capital:
            logger.warning(f"资金不足，无法开仓: {symbol}")
            return
            
        # 记录持仓
        self.positions[symbol] = {
            'direction': direction,
            'size': size,
            'entry_price': current_price,
            'stop_loss': signal['stop_loss'],
            'take_profit': signal['take_profit'],
            'entry_time': signal['timestamp']
        }
        
        # 更新资金
        self.current_capital -= total_cost
        
        # 记录交易
        self.trades.append({
            'symbol': symbol,
            'direction': direction,
            'size': size,
            'price': current_price,
            'timestamp': signal['timestamp'],
            'type': 'open',
            'cost': total_cost
        })
        
    def _close_position(self, symbol: str, current_price: float, timestamp: pd.Timestamp, reason: str):
        """
        平仓
        :param symbol: 交易对
        :param current_price: 当前价格
        :param timestamp: 时间戳
        :param reason: 平仓原因
        """
        position = self.positions[symbol]
        
        # 计算盈亏
        pnl = position['direction'] * position['size'] * (current_price - position['entry_price'])
        
        # 计算交易成本
        commission = position['size'] * current_price * COMMISSION_RATE
        slippage = position['size'] * current_price * SLIPPAGE
        total_cost = commission + slippage
        
        # 更新资金
        self.current_capital += pnl - total_cost
        
        # 记录交易
        self.trades.append({
            'symbol': symbol,
            'direction': -position['direction'],
            'size': position['size'],
            'price': current_price,
            'timestamp': timestamp,
            'type': 'close',
            'reason': reason,
            'pnl': pnl,
            'cost': total_cost
        })
        
        # 移除持仓
        del self.positions[symbol]
        
    def _calculate_total_equity(self, current_price: float) -> float:
        """
        计算总权益
        :param current_price: 当前价格
        :return: 总权益
        """
        total_equity = self.current_capital
        
        for position in self.positions.values():
            unrealized_pnl = position['direction'] * position['size'] * (current_price - position['entry_price'])
            total_equity += unrealized_pnl
            
        return total_equity
        
    def _calculate_results(self) -> Dict:
        """
        计算回测结果
        :return: 回测结果字典
        """
        if not self.trades:
            return {
                'total_return': 0,
                'sharpe_ratio': 0,
                'max_drawdown': 0,
                'win_rate': 0,
                'total_trades': 0,
                'profit_factor': 0
            }
            
        # 计算收益率
        total_return = (self.current_capital - self.initial_capital) / self.initial_capital
        
        # 计算夏普比率
        returns = pd.Series([t['pnl'] for t in self.trades if t['type'] == 'close'])
        sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std() if len(returns) > 1 else 0
        
        # 计算最大回撤
        equity_curve = pd.DataFrame(self.equity_curve)
        rolling_max = equity_curve['equity'].expanding().max()
        drawdowns = (equity_curve['equity'] - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()
        
        # 计算胜率
        winning_trades = len([t for t in self.trades if t['type'] == 'close' and t['pnl'] > 0])
        total_trades = len([t for t in self.trades if t['type'] == 'close'])
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        # 计算盈亏比
        gross_profit = sum([t['pnl'] for t in self.trades if t['type'] == 'close' and t['pnl'] > 0])
        gross_loss = abs(sum([t['pnl'] for t in self.trades if t['type'] == 'close' and t['pnl'] < 0]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'total_trades': total_trades,
            'profit_factor': profit_factor,
            'trades': self.trades,
            'equity_curve': self.equity_curve
        } 