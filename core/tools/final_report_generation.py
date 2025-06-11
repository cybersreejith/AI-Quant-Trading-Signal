from typing import Dict, Any, List, Optional
import logging
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field
from datetime import datetime
from langchain_core.tools import tool
import json

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

class FinalTradingReport(BaseModel):
    """Complete trading report with all data for frontend"""
    quant_analysis: dict = Field(description="quantitative analysis result")
    market_sentiment: dict = Field(description="market sentiment analysis result")
    ai_analysis: str = Field(description="AI generated comprehensive analysis report text")
    generated_at: str = Field(description="generation time")

class ReportAgent:
    """Trading analysis report generation AI agent"""
    
    def __init__(self, model_name: str = "gpt-4o"):
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
            ("system", """You are a professional quantitative trading analyst. Please generate a comprehensive analysis report based on the provided quantitative analysis and market sentiment data.

            Please analyze the input data and generate a JSON format with a single field containing a complete report:
            {{
                "summary": "Here is the complete analysis report text, including:\n1. Strategy performance summary\n2. Market sentiment analysis\n3. Recommendations\n4. Risk assessment\n5. Conclusion and recommendations"
            }}
            
            Requirements:
            1. Output ONLY valid JSON format with single "summary" field
            2. The report should be a complete, well-structured analysis (300-500 words)
            3. Include strategy performance, market sentiment, recommendations, and risk assessment
            4. Use clear section headers and bullet points for readability
            5. Provide specific actionable advice
            6. Use English for all content
            7. DO NOT include any text outside the JSON structure"""),
            ("user", "{analysis_data}")
        ])
        
        # no need for Pydantic output parser, directly parse JSON
    
    def generate_report(self, quant_analysis_result: Dict[str, Any], market_sentiment_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis report based on the provided quantitative analysis and market sentiment analysis
        """
        try:
            logger.info("Starting to generate trading analysis report")
            
            # Merge two JSON objects as input data
            combined_data = {
                "quant_analysis": quant_analysis_result,
                "market_sentiment": market_sentiment_result
            }
            
            # Call model to generate report
            response = self.model.invoke(
                self.report_prompt.format(analysis_data=json.dumps(combined_data, ensure_ascii=False, indent=2))
            )
            
            # Parse LLM output JSON directly
            logger.info(f"LLM raw response: {response.content}")
            try:
                llm_output = json.loads(response.content)
                summary_text = llm_output.get("summary", "Failed to generate report")
                logger.info(f"Successfully parsed LLM JSON output")
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed: {str(e)}")
                logger.error(f"Raw content: {response.content}")
                
                # Try to extract content between JSON markers if LLM wrapped it
                content = response.content.strip()
                if "```json" in content and "```" in content:
                    # Extract JSON from markdown code block
                    start = content.find("```json") + 7
                    end = content.rfind("```")
                    json_content = content[start:end].strip()
                    try:
                        llm_output = json.loads(json_content)
                        summary_text = llm_output.get("summary", "Failed to generate report")
                        logger.info(f"Successfully extracted JSON from markdown")
                    except:
                        summary_text = f"Error: Could not parse LLM response. Raw content: {content[:200]}..."
                else:
                    # If no valid JSON found, use the raw content as summary
                    summary_text = f"LLM Response (non-JSON): {content}"
            
            # Create complete report with all data for frontend
            complete_report = FinalTradingReport(
                quant_analysis=quant_analysis_result,
                market_sentiment=market_sentiment_result,
                ai_analysis=summary_text,
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            report_dict = complete_report.model_dump()
            logger.info(f"Complete trading analysis report generated: {report_dict}")
            return report_dict
            
        except Exception as e:
            logger.error(f"Error generating trading analysis report: {str(e)}")
            return {
                "error": str(e)
            }

# create global agent instance  
_report_agent = ReportAgent()

@tool("generate_report")        
def generate_report(quant_analysis_result: Dict[str, Any], market_sentiment_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a comprehensive analysis report based on the provided quantitative analysis and market sentiment analysis
    """
    return _report_agent.generate_report(quant_analysis_result, market_sentiment_result) 