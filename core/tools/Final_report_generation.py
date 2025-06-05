from typing import Dict, Any, List, Optional
import logging
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found, please make sure your .env file is configured correctly")
    raise ValueError("OPENAI_API_KEY not found, please make sure your .env file is configured correctly")

class TradingReport(BaseModel):
    """Trading analysis report model"""
    summary: str = Field(description="Report summary")
    backtest_analysis: Dict[str, Any] = Field(description="Backtest result analysis")
    live_signal_analysis: Dict[str, Any] = Field(description="Live signal analysis")
    sentiment_analysis: Dict[str, Any] = Field(description="Market sentiment analysis")
    recommendations: List[str] = Field(description="Trading recommendations")
    risk_assessment: Dict[str, Any] = Field(description="Risk assessment")
    confidence_score: float = Field(description="Overall analysis confidence")

class ReportAgent:
    """Trading analysis report generation AI agent"""
    
    def __init__(self, model_name: str = "gpt-4"):
        """
        Initialize the report generation AI agent
        
        Args:
            model_name: The name of the model to use
        """
        self.model = ChatOpenAI(
            model_name=model_name,
            temperature=0,
            openai_api_key=OPENAI_API_KEY
        )
        self._setup_prompts()
        
    def _setup_prompts(self) -> None:
        """Set up the prompt template"""
        # Report generation prompt template
        self.report_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional quantitative trading analyst. Please generate a comprehensive trading analysis report based on the following data:
            
            1. Backtest result analysis:
               - Strategy performance evaluation
               - Key metrics analysis
               - Risk-return characteristics
               
            2. Live signal analysis:
               - Current market state
               - Signal reliability assessment
               - Technical indicator interpretation
               
            3. Market sentiment analysis:
               - Overall sentiment assessment
               - Key influencing factors
               - News event impact
               
            4. Comprehensive recommendations:
               - Trading decision recommendations
               - Risk management recommendations
               - Follow-up focus points
               
            Ensure the report:
            - Clear logic, prominent focus
            - Data support sufficient
            - Recommendations specific and feasible
            - Comprehensive risk assessment"""),
            ("user", "{analysis_data}")
        ])
        
        # Output parser
        self.output_parser = PydanticOutputParser(pydantic_object=TradingReport)
        
    def _format_analysis_data(self, data: Dict[str, Any]) -> str:
        """
        Format analysis data
        
        Args:
            data: Data containing backtest results, live signals, and market sentiment
            
        Returns:
            Formatted analysis data text
        """
        try:
            formatted_data = []
            
            # Backtest results
            if "backtest_results" in data:
                backtest = data["backtest_results"]
                formatted_data.append("=== Backtest results ===")
                formatted_data.append(f"Total return: {backtest.get('total_return', 'N/A')}")
                formatted_data.append(f"Annual return: {backtest.get('annual_return', 'N/A')}")
                formatted_data.append(f"Max drawdown: {backtest.get('max_drawdown', 'N/A')}")
                formatted_data.append(f"Sharpe ratio: {backtest.get('sharpe_ratio', 'N/A')}")
                formatted_data.append(f"Win rate: {backtest.get('win_rate', 'N/A')}")
                
            # Live signal
            if "live_signal" in data:
                signal = data["live_signal"]
                formatted_data.append("\n=== Live signal ===")
                formatted_data.append(f"Signal type: {signal.get('signal', 'N/A')}")
                formatted_data.append(f"Generated time: {signal.get('timestamp', 'N/A')}")
                formatted_data.append(f"Current price: {signal.get('price', 'N/A')}")
                formatted_data.append("Technical indicators:")
                for indicator, value in signal.get('indicators', {}).items():
                    formatted_data.append(f"  - {indicator}: {value}")
                    
            # Market sentiment
            if "sentiment_analysis" in data:
                sentiment = data["sentiment_analysis"]
                formatted_data.append("\n=== Market sentiment ===")
                formatted_data.append(f"Overall sentiment: {sentiment.get('overall_sentiment', 'N/A')}")
                formatted_data.append(f"Sentiment score: {sentiment.get('sentiment_score', 'N/A')}")
                formatted_data.append(f"Confidence: {sentiment.get('confidence', 'N/A')}")
                formatted_data.append("Key points:")
                for point in sentiment.get('key_points', []):
                    formatted_data.append(f"  - {point}")
                formatted_data.append(f"News summary: {sentiment.get('news_summary', 'N/A')}")
                
            return "\n".join(formatted_data)
            
        except Exception as e:
            logger.error(f"Error formatting analysis data: {str(e)}")
            return str(data)
            
    def generate_report(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate trading analysis report
        
        Args:
            analysis_data: Data containing backtest results, live signals, and market sentiment
            
        Returns:
            Generated trading analysis report
        """
        try:
            logger.info("Starting to generate trading analysis report")
            
            # Format analysis data
            formatted_data = self._format_analysis_data(analysis_data)
            
            # Call model to generate report
            response = self.model.predict(
                self.report_prompt.format(analysis_data=formatted_data)
            )
            
            # Parse output
            report = self.output_parser.parse(response)
            
            # Add timestamp
            report_dict = report.dict()
            report_dict["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            logger.info("Trading analysis report generated")
            return report_dict
            
        except Exception as e:
            logger.error(f"Error generating trading analysis report: {str(e)}")
            return {
                "error": str(e)
            } 