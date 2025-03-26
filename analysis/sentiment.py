import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from utils.logger import setup_logger
from config.settings import OPENAI_API_KEY
import openai

logger = setup_logger(__name__)
openai.api_key = OPENAI_API_KEY

def analyze_market_sentiment(data: pd.DataFrame, symbol: str) -> Dict:
    """
    分析市场情绪
    :param data: 包含价格和技术指标数据的DataFrame
    :param symbol: 交易对符号
    :return: 市场情绪分析结果
    """
    try:
        # 准备市场数据摘要
        market_summary = prepare_market_summary(data)
        
        # 调用OpenAI API进行情绪分析
        sentiment_analysis = get_ai_sentiment_analysis(market_summary)
        
        # 解析AI分析结果
        sentiment_score = sentiment_analysis['sentiment_score']
        sentiment_reasoning = sentiment_analysis['sentiment_reasoning']
        
        logger.info(f"完成{symbol}的市场情绪分析")
        return {
            'symbol': symbol,
            'sentiment_score': sentiment_score,
            'sentiment_reasoning': sentiment_reasoning,
            'timestamp': pd.Timestamp.now()
        }
        
    except Exception as e:
        logger.error(f"市场情绪分析出错: {str(e)}")
        return None

def prepare_market_summary(data: pd.DataFrame) -> str:
    """
    准备市场数据摘要
    :param data: 包含价格和技术指标数据的DataFrame
    :return: 市场数据摘要文本
    """
    latest = data.iloc[-1]
    summary = f"""
    最新价格: {latest['CLOSE']:.2f}
    24小时涨跌幅: {((latest['CLOSE'] - data.iloc[-2]['CLOSE']) / data.iloc[-2]['CLOSE'] * 100):.2f}%
    
    技术指标:
    - RSI: {latest['RSI']:.2f}
    - MACD: {latest['MACD']:.2f}
    - 布林带位置: {'上轨' if latest['CLOSE'] > latest['UPPER'] else '中轨' if latest['CLOSE'] > latest['MIDDLE'] else '下轨'}
    - ADX: {latest['ADX']:.2f}
    
    趋势指标:
    - 20日均线: {latest['SMA20']:.2f}
    - 50日均线: {latest['SMA50']:.2f}
    - 200日均线: {latest['SMA200']:.2f}
    """
    return summary

def get_ai_sentiment_analysis(market_summary: str) -> Dict:
    """
    使用 OpenAI API 分析市场情绪
    :param market_summary: 市场数据摘要
    :return: 情绪分析结果
    """
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的量化交易分析师，请根据提供的市场数据，分析市场情绪并给出情绪得分（-1到1之间）和详细分析。"},
                {"role": "user", "content": market_summary}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # 解析响应
        sentiment_text = response.choices[0].message.content
        sentiment_score = parse_sentiment_score(sentiment_text)
        sentiment_reasoning = parse_sentiment_reasoning(sentiment_text)
        
        return {
            'sentiment_score': sentiment_score,
            'sentiment_reasoning': sentiment_reasoning
        }
        
    except Exception as e:
        logger.error(f"OpenAI API调用失败: {str(e)}")
        return None

def parse_sentiment_score(analysis: str) -> float:
    """
    解析情绪评分
    :param analysis: AI分析结果
    :return: 情绪评分
    """
    try:
        import json
        result = json.loads(analysis)
        return float(result['sentiment_score'])
    except:
        return 0.0

def parse_sentiment_reasoning(analysis: str) -> str:
    """
    解析分析理由
    :param analysis: AI分析结果
    :return: 分析理由
    """
    try:
        import json
        result = json.loads(analysis)
        return result['reasoning']
    except:
        return "无法解析分析理由" 