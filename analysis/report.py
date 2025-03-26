import pandas as pd
import numpy as np
from typing import Dict, List
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
        self.report_dir = 'reports'
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
            
    def generate_report(self, backtest_results: Dict, sentiment_analysis: Dict) -> str:
        """
        生成完整的交易分析报告
        :param backtest_results: 回测结果
        :param sentiment_analysis: 市场情绪分析结果
        :return: 报告文件路径
        """
        try:
            # 生成报告文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = f'{self.report_dir}/trading_report_{timestamp}.html'
            
            # 生成图表
            self._generate_charts(backtest_results)
            
            # 生成报告内容
            report_content = self._generate_report_content(backtest_results, sentiment_analysis)
            
            # 保存报告
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
                
            logger.info(f"报告已生成: {report_file}")
            return report_file
            
        except Exception as e:
            logger.error(f"生成报告时出错: {str(e)}")
            return None
            
    def _generate_charts(self, backtest_results: Dict):
        """
        生成图表
        :param backtest_results: 回测结果
        """
        # 设置图表风格
        plt.style.use('seaborn')
        
        # 生成权益曲线图
        equity_curve = pd.DataFrame(backtest_results['equity_curve'])
        plt.figure(figsize=(12, 6))
        plt.plot(equity_curve['timestamp'], equity_curve['equity'])
        plt.title('权益曲线')
        plt.xlabel('时间')
        plt.ylabel('权益')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.report_dir}/equity_curve.png')
        plt.close()
        
        # 生成回撤图
        rolling_max = equity_curve['equity'].expanding().max()
        drawdowns = (equity_curve['equity'] - rolling_max) / rolling_max
        plt.figure(figsize=(12, 6))
        plt.plot(equity_curve['timestamp'], drawdowns)
        plt.title('回撤曲线')
        plt.xlabel('时间')
        plt.ylabel('回撤')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.report_dir}/drawdown.png')
        plt.close()
        
        # 生成月度收益热力图
        trades_df = pd.DataFrame(backtest_results['trades'])
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        trades_df['month'] = trades_df['timestamp'].dt.to_period('M')
        monthly_returns = trades_df[trades_df['type'] == 'close'].groupby('month')['pnl'].sum()
        
        monthly_returns_matrix = monthly_returns.unstack()
        plt.figure(figsize=(12, 8))
        sns.heatmap(monthly_returns_matrix, annot=True, fmt='.2f', cmap='RdYlGn')
        plt.title('月度收益热力图')
        plt.tight_layout()
        plt.savefig(f'{self.report_dir}/monthly_returns.png')
        plt.close()
        
    def _generate_report_content(self, backtest_results: Dict, sentiment_analysis: Dict) -> str:
        """
        生成报告内容
        :param backtest_results: 回测结果
        :param sentiment_analysis: 市场情绪分析结果
        :return: HTML格式的报告内容
        """
        # 准备报告数据
        performance_metrics = {
            '总收益率': f"{backtest_results['total_return']*100:.2f}%",
            '夏普比率': f"{backtest_results['sharpe_ratio']:.2f}",
            '最大回撤': f"{backtest_results['max_drawdown']*100:.2f}%",
            '胜率': f"{backtest_results['win_rate']*100:.2f}%",
            '总交易次数': str(backtest_results['total_trades']),
            '盈亏比': f"{backtest_results['profit_factor']:.2f}"
        }
        
        # 生成HTML报告
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>交易分析报告</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .section {{ margin-bottom: 30px; }}
                .metric-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
                .metric-card {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
                .chart {{ text-align: center; margin: 20px 0; }}
                .chart img {{ max-width: 100%; height: auto; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
                th {{ background: #f5f5f5; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>交易分析报告</h1>
                    <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="section">
                    <h2>性能指标</h2>
                    <div class="metric-grid">
                        {''.join([f'<div class="metric-card"><h3>{k}</h3><p>{v}</p></div>' for k, v in performance_metrics.items()])}
                    </div>
                </div>
                
                <div class="section">
                    <h2>市场情绪分析</h2>
                    <div class="metric-card">
                        <h3>情绪得分</h3>
                        <p>{sentiment_analysis['sentiment_score']:.2f}</p>
                        <h3>分析理由</h3>
                        <p>{sentiment_analysis['sentiment_reasoning']}</p>
                    </div>
                </div>
                
                <div class="section">
                    <h2>图表分析</h2>
                    <div class="chart">
                        <h3>权益曲线</h3>
                        <img src="equity_curve.png" alt="权益曲线">
                    </div>
                    <div class="chart">
                        <h3>回撤曲线</h3>
                        <img src="drawdown.png" alt="回撤曲线">
                    </div>
                    <div class="chart">
                        <h3>月度收益热力图</h3>
                        <img src="monthly_returns.png" alt="月度收益热力图">
                    </div>
                </div>
                
                <div class="section">
                    <h2>交易记录</h2>
                    <table>
                        <tr>
                            <th>时间</th>
                            <th>交易对</th>
                            <th>方向</th>
                            <th>价格</th>
                            <th>数量</th>
                            <th>盈亏</th>
                            <th>原因</th>
                        </tr>
                        {''.join([f"""
                        <tr>
                            <td>{t['timestamp']}</td>
                            <td>{t['symbol']}</td>
                            <td>{'买入' if t['direction'] > 0 else '卖出'}</td>
                            <td>{t['price']:.2f}</td>
                            <td>{t['size']:.4f}</td>
                            <td>{t.get('pnl', 0):.2f}</td>
                            <td>{t.get('reason', '')}</td>
                        </tr>
                        """ for t in backtest_results['trades'] if t['type'] == 'close'])}
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content 