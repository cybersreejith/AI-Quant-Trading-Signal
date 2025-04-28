from typing import Dict, Any, List, Optional
import logging
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from datetime import datetime

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

class TradingReport(BaseModel):
    """交易分析报告模型"""
    summary: str = Field(description="报告摘要")
    backtest_analysis: Dict[str, Any] = Field(description="回测结果分析")
    live_signal_analysis: Dict[str, Any] = Field(description="实时信号分析")
    sentiment_analysis: Dict[str, Any] = Field(description="市场情绪分析")
    recommendations: List[str] = Field(description="交易建议")
    risk_assessment: Dict[str, Any] = Field(description="风险评估")
    confidence_score: float = Field(description="整体分析置信度")

class ReportAgent:
    """交易分析报告生成AI agent"""
    
    def __init__(self, model_name: str = "gpt-4"):
        """
        初始化报告生成AI agent
        
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
        # 报告生成提示模板
        self.report_prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的量化交易分析师。请基于以下数据生成一份全面的交易分析报告：
            
            1. 回测结果分析：
               - 策略表现评估
               - 关键指标分析
               - 风险收益特征
               
            2. 实时信号分析：
               - 当前市场状态
               - 信号可靠性评估
               - 技术指标解读
               
            3. 市场情绪分析：
               - 整体情绪评估
               - 关键影响因素
               - 新闻事件影响
               
            4. 综合建议：
               - 交易决策建议
               - 风险管理建议
               - 后续关注点
               
            请确保报告：
            - 逻辑清晰，重点突出
            - 数据支持充分
            - 建议具体可行
            - 风险评估全面"""),
            ("user", "{analysis_data}")
        ])
        
        # 输出解析器
        self.output_parser = PydanticOutputParser(pydantic_object=TradingReport)
        
    def _format_analysis_data(self, data: Dict[str, Any]) -> str:
        """
        格式化分析数据
        
        Args:
            data: 包含回测结果、实时信号和市场情绪的数据
            
        Returns:
            格式化的分析数据文本
        """
        try:
            formatted_data = []
            
            # 回测结果
            if "backtest_results" in data:
                backtest = data["backtest_results"]
                formatted_data.append("=== 回测结果 ===")
                formatted_data.append(f"总收益率: {backtest.get('total_return', 'N/A')}")
                formatted_data.append(f"年化收益率: {backtest.get('annual_return', 'N/A')}")
                formatted_data.append(f"最大回撤: {backtest.get('max_drawdown', 'N/A')}")
                formatted_data.append(f"夏普比率: {backtest.get('sharpe_ratio', 'N/A')}")
                formatted_data.append(f"胜率: {backtest.get('win_rate', 'N/A')}")
                
            # 实时信号
            if "live_signal" in data:
                signal = data["live_signal"]
                formatted_data.append("\n=== 实时信号 ===")
                formatted_data.append(f"信号类型: {signal.get('signal', 'N/A')}")
                formatted_data.append(f"生成时间: {signal.get('timestamp', 'N/A')}")
                formatted_data.append(f"当前价格: {signal.get('price', 'N/A')}")
                formatted_data.append("技术指标:")
                for indicator, value in signal.get('indicators', {}).items():
                    formatted_data.append(f"  - {indicator}: {value}")
                    
            # 市场情绪
            if "sentiment_analysis" in data:
                sentiment = data["sentiment_analysis"]
                formatted_data.append("\n=== 市场情绪 ===")
                formatted_data.append(f"整体情绪: {sentiment.get('overall_sentiment', 'N/A')}")
                formatted_data.append(f"情绪得分: {sentiment.get('sentiment_score', 'N/A')}")
                formatted_data.append(f"置信度: {sentiment.get('confidence', 'N/A')}")
                formatted_data.append("关键点:")
                for point in sentiment.get('key_points', []):
                    formatted_data.append(f"  - {point}")
                formatted_data.append(f"新闻摘要: {sentiment.get('news_summary', 'N/A')}")
                
            return "\n".join(formatted_data)
            
        except Exception as e:
            logger.error(f"格式化分析数据时出错: {str(e)}")
            return str(data)
            
    def generate_report(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成交易分析报告
        
        Args:
            analysis_data: 包含回测结果、实时信号和市场情绪的数据
            
        Returns:
            生成的交易分析报告
        """
        try:
            logger.info("开始生成交易分析报告")
            
            # 格式化分析数据
            formatted_data = self._format_analysis_data(analysis_data)
            
            # 调用模型生成报告
            response = self.model.predict(
                self.report_prompt.format(analysis_data=formatted_data)
            )
            
            # 解析输出
            report = self.output_parser.parse(response)
            
            # 添加时间戳
            report_dict = report.dict()
            report_dict["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            logger.info("交易分析报告生成完成")
            return report_dict
            
        except Exception as e:
            logger.error(f"生成交易分析报告时出错: {str(e)}")
            return {
                "error": str(e)
            } 