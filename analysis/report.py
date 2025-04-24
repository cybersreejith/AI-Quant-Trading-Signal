import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from utils.logger import setup_logger
from config.settings import OPENAI_API_KEY
import openai
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

logger = setup_logger(__name__)
openai.api_key = OPENAI_API_KEY

class ReportGenerator:
    """
    报告生成器
    """
    def __init__(self):
        # 创建reports目录
        if not os.path.exists('reports'):
            os.makedirs('reports')
            
    def generate_report(
        self,
        backtest_results: Dict,
        market_sentiment: Dict
    ) -> Optional[str]:
        """
        生成交易分析报告
        :param backtest_results: 回测结果
        :param market_sentiment: 市场情绪分析结果
        :return: 报告文件路径
        """
        try:
            # 生成报告文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"reports/trading_report_{timestamp}.txt"
            
            # 生成报告内容
            report_content = self._generate_report_content(
                backtest_results,
                market_sentiment
            )
            
            # 保存报告
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
                
            # 生成图表
            self._generate_charts(backtest_results, timestamp)
            
            logger.info(f"报告已生成: {report_file}")
            return report_file
            
        except Exception as e:
            logger.error(f"生成报告时出错: {str(e)}")
            return None
            
    def _generate_report_content(
        self,
        backtest_results: Dict,
        market_sentiment: Dict
    ) -> str:
        """
        生成报告内容
        """
        content = []
        
        # 添加报告标题
        content.append("交易分析报告")
        content.append("=" * 50)
        content.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")
        
        # 添加市场情绪分析
        content.append("市场情绪分析")
        content.append("-" * 30)
        content.append(f"情绪得分: {market_sentiment['sentiment_score']:.2f}")
        content.append(f"分析原因: {market_sentiment['sentiment_reasoning']}")
        content.append("")
        
        # 添加回测结果
        content.append("回测结果")
        content.append("-" * 30)
        content.append(f"初始资金: ${backtest_results['initial_capital']:,.2f}")
        content.append(f"最终资金: ${backtest_results['final_capital']:,.2f}")
        content.append(f"总收益率: {backtest_results['total_return']:.2%}")
        content.append(f"年化收益率: {backtest_results['annual_return']:.2%}")
        content.append(f"最大回撤: {backtest_results['max_drawdown']:.2%}")
        content.append(f"夏普比率: {backtest_results['sharpe_ratio']:.2f}")
        content.append("")
        
        # 添加交易统计
        content.append("交易统计")
        content.append("-" * 30)
        content.append(f"总交易次数: {backtest_results['total_trades']}")
        content.append(f"盈利交易: {backtest_results['winning_trades']}")
        content.append(f"亏损交易: {backtest_results['losing_trades']}")
        content.append(f"胜率: {backtest_results['win_rate']:.2%}")
        content.append(f"平均盈利: {backtest_results['avg_profit']:.2%}")
        content.append(f"平均亏损: {backtest_results['avg_loss']:.2%}")
        content.append("")
        
        # 添加风险指标
        content.append("风险指标")
        content.append("-" * 30)
        content.append(f"波动率: {backtest_results['volatility']:.2%}")
        content.append(f"下行风险: {backtest_results['downside_risk']:.2%}")
        content.append(f"索提诺比率: {backtest_results['sortino_ratio']:.2f}")
        
        return "\n".join(content)
        
    def _generate_charts(self, backtest_results: Dict, timestamp: str):
        """
        生成图表
        """
        try:
            # 创建图表目录
            charts_dir = f"reports/charts_{timestamp}"
            if not os.path.exists(charts_dir):
                os.makedirs(charts_dir)
                
            # 绘制权益曲线
            plt.figure(figsize=(12, 6))
            plt.plot(backtest_results['equity_curve']['timestamp'],
                    backtest_results['equity_curve']['equity'])
            plt.title("权益曲线")
            plt.xlabel("时间")
            plt.ylabel("权益")
            plt.grid(True)
            plt.savefig(f"{charts_dir}/equity_curve.png")
            plt.close()
            
            # 绘制回撤曲线
            plt.figure(figsize=(12, 6))
            plt.plot(backtest_results['drawdown_curve']['timestamp'],
                    backtest_results['drawdown_curve']['drawdown'])
            plt.title("回撤曲线")
            plt.xlabel("时间")
            plt.ylabel("回撤")
            plt.grid(True)
            plt.savefig(f"{charts_dir}/drawdown_curve.png")
            plt.close()
            
            # 绘制月度收益热力图
            monthly_returns = pd.DataFrame(backtest_results['monthly_returns'])
            plt.figure(figsize=(12, 8))
            sns.heatmap(monthly_returns, annot=True, fmt='.2%', cmap='RdYlGn')
            plt.title("月度收益热力图")
            plt.savefig(f"{charts_dir}/monthly_returns.png")
            plt.close()
            
            logger.info(f"图表已生成: {charts_dir}")
            
        except Exception as e:
            logger.error(f"生成图表时出错: {str(e)}") 