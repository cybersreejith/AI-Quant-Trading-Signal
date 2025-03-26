import pandas as pd
from typing import List, Dict, Optional
from utils.logger import setup_logger
from utils.email import send_email
from core.data import fetch_asset_data
from core.indicators import calculate_indicators
from core.strategy import TunableClassicTrendFollow
from core.backtest import Backtest
from analysis.sentiment import analyze_market_sentiment
from analysis.report import ReportGenerator
from config.settings import (
    TRADING_PAIRS,
    START_DATE,
    END_DATE,
    EMAIL_RECIPIENTS,
    EMAIL_SUBJECT
)

logger = setup_logger(__name__)

def process_trading_signals(
    trading_pairs: List[str],
    start_date: str,
    end_date: str
) -> Optional[List[Dict]]:
    """
    处理交易信号
    :param trading_pairs: 交易对列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 交易信号列表
    """
    trading_signals = []
    
    for symbol in trading_pairs:
        logger.info(f"开始分析交易对: {symbol}")
        
        # 获取历史数据
        historical_data = fetch_asset_data(symbol, start_date, end_date)
        if historical_data is None:
            continue
            
        # 计算技术指标
        technical_data = calculate_indicators(historical_data)
        if technical_data is None:
            continue
            
        # 分析市场情绪
        market_sentiment = analyze_market_sentiment(technical_data, symbol)
        if market_sentiment is None:
            continue
            
        # 生成交易信号
        trading_signal = strategy.analyze_single_asset(
            technical_data,
            market_sentiment['sentiment_score']
        )
        if trading_signal is not None:
            trading_signals.append(trading_signal)
            
    return trading_signals

def generate_and_send_report(
    backtest_results: Dict,
    market_sentiment: Dict,
    report_generator: ReportGenerator
) -> bool:
    """
    生成并发送报告
    :param backtest_results: 回测结果
    :param market_sentiment: 市场情绪分析结果
    :param report_generator: 报告生成器实例
    :return: 是否成功
    """
    try:
        # 生成报告
        report_file = report_generator.generate_report(
            backtest_results,
            market_sentiment
        )
        
        if report_file is None:
            logger.error("报告生成失败")
            return False
            
        # 准备邮件内容
        email_content = f"""
        尊敬的交易者：
        
        附件是您的交易分析报告。报告包含了以下内容：
        1. 性能指标（总收益率、夏普比率、最大回撤等）
        2. 市场情绪分析
        3. 图表分析（权益曲线、回撤曲线、月度收益热力图）
        4. 详细交易记录
        
        请查看附件获取完整报告。
        """
        
        # 发送邮件
        success = send_email(
            recipients=EMAIL_RECIPIENTS,
            subject=EMAIL_SUBJECT,
            body=email_content,
            attachments=[report_file]
        )
        
        if success:
            logger.info("报告已成功发送")
        else:
            logger.error("报告发送失败")
            
        return success
        
    except Exception as e:
        logger.error(f"发送报告时出错: {str(e)}")
        return False

def run_trading_analysis() -> None:
    """
    运行交易分析主程序
    """
    try:
        # 初始化组件
        strategy = TunableClassicTrendFollow()
        backtest = Backtest()
        report_generator = ReportGenerator()
        
        # 处理交易信号
        trading_signals = process_trading_signals(
            TRADING_PAIRS,
            START_DATE,
            END_DATE
        )
        
        if not trading_signals:
            logger.warning("没有生成任何交易信号")
            return
            
        # 获取最新数据用于回测
        latest_symbol = trading_signals[-1]['symbol']
        historical_data = fetch_asset_data(latest_symbol, START_DATE, END_DATE)
        if historical_data is None:
            logger.error("获取历史数据失败")
            return
            
        # 计算技术指标
        technical_data = calculate_indicators(historical_data)
        if technical_data is None:
            logger.error("计算技术指标失败")
            return
            
        # 分析市场情绪
        market_sentiment = analyze_market_sentiment(technical_data, latest_symbol)
        if market_sentiment is None:
            logger.error("市场情绪分析失败")
            return
            
        # 运行回测
        backtest_results = backtest.run(technical_data, trading_signals)
        if backtest_results is None:
            logger.error("回测失败")
            return
            
        # 生成并发送报告
        success = generate_and_send_report(
            backtest_results,
            market_sentiment,
            report_generator
        )
        
        if not success:
            logger.error("报告生成和发送失败")
            
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        
if __name__ == "__main__":
    run_trading_analysis() 