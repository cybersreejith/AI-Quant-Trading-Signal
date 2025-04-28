from typing import Dict, Any, List, Optional
import logging
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import json
import yfinance as yf

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("未找到 OPENAI_API_KEY，请确保.env文件已正确配置")
    raise ValueError("未找到 OPENAI_API_KEY，请确保.env文件已正确配置")

class NewsArticle(BaseModel):
    """新闻文章模型"""
    title: str = Field(description="新闻标题")
    source: str = Field(description="新闻来源")
    date: str = Field(description="发布日期")
    summary: str = Field(description="新闻摘要")
    url: str = Field(description="新闻链接")

class SentimentAnalysis(BaseModel):
    """市场情绪分析结果模型"""
    overall_sentiment: str = Field(description="整体市场情绪：积极/中性/消极")
    sentiment_score: float = Field(description="情绪得分，范围-1到1")
    key_points: List[str] = Field(description="关键点分析")
    confidence: float = Field(description="分析置信度，范围0到1")
    news_summary: str = Field(description="新闻内容总结")

class SentimentAgent:
    """市场情绪分析AI agent"""
    
    def __init__(self, model_name: str = "gpt-4"):
        """
        初始化市场情绪分析AI agent
        
        Args:
            model_name: 使用的模型名称
        """
        self.model = ChatOpenAI(
            model_name=model_name,
            temperature=0,
            openai_api_key=OPENAI_API_KEY
        )
        self._setup_prompts()
        
    def _setup_prompts(self) -> None:
        """设置提示模板"""
        # 新闻分析提示模板
        self.news_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的市场情绪分析师。请分析以下新闻内容，提取关键信息并评估市场情绪。
            请按照以下格式输出：
            1. 整体市场情绪（积极/中性/消极）
            2. 情绪得分（-1到1）
            3. 关键点分析（列表形式）
            4. 分析置信度（0到1）
            5. 新闻内容总结（200字以内）"""),
            ("user", "{news_content}")
        ])
        
        # 输出解析器
        self.output_parser = PydanticOutputParser(pydantic_object=SentimentAnalysis)
        
    def _fetch_news(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        获取资产相关新闻
        
        Args:
            symbol: 资产代码
            days: 获取最近几天的新闻
            
        Returns:
            新闻列表
        """
        try:
            # 使用 yfinance 获取新闻
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            # 格式化新闻数据
            formatted_articles = []
            for article in news:
                # 转换时间戳为日期字符串
                date = datetime.fromtimestamp(article['providerPublishTime']).strftime('%Y-%m-%d %H:%M:%S')
                
                formatted_articles.append({
                    "title": article['title'],
                    "source": article['publisher'],
                    "date": date,
                    "summary": article.get('summary', ''),
                    "url": article['link']
                })
                
            return formatted_articles
            
        except Exception as e:
            logger.error(f"获取新闻时出错: {str(e)}")
            return []
            
    def _analyze_news(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析新闻内容
        
        Args:
            articles: 新闻文章列表
            
        Returns:
            分析结果
        """
        try:
            # 合并新闻内容
            news_content = "\n\n".join([
                f"标题: {article['title']}\n"
                f"来源: {article['source']}\n"
                f"日期: {article['date']}\n"
                f"摘要: {article['summary']}\n"
                for article in articles
            ])
            
            # 调用模型分析
            response = self.model.predict(
                self.news_analysis_prompt.format(news_content=news_content)
            )
            
            # 解析输出
            analysis = self.output_parser.parse(response)
            
            return {
                "overall_sentiment": analysis.overall_sentiment,
                "sentiment_score": analysis.sentiment_score,
                "key_points": analysis.key_points,
                "confidence": analysis.confidence,
                "news_summary": analysis.news_summary,
                "articles": articles
            }
            
        except Exception as e:
            logger.error(f"分析新闻时出错: {str(e)}")
            return {
                "error": str(e)
            }
            
    def analyze_market_sentiment(self, symbol: str) -> Dict[str, Any]:
        """
        分析市场情绪
        
        Args:
            symbol: 资产代码
            
        Returns:
            市场情绪分析结果
        """
        try:
            logger.info(f"开始分析 {symbol} 的市场情绪")
            
            # 获取新闻
            articles = self._fetch_news(symbol)
            if not articles:
                logger.warning(f"未找到 {symbol} 的相关新闻")
                return {
                    "error": "未找到相关新闻"
                }
                
            # 分析新闻
            result = self._analyze_news(articles)
            
            logger.info(f"{symbol} 的市场情绪分析完成")
            return result
            
        except Exception as e:
            logger.error(f"分析市场情绪时出错: {str(e)}")
            return {
                "error": str(e)
            } 