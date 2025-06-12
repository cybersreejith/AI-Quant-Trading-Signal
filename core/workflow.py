from typing import TypedDict, Annotated, Sequence, Dict, Any, NotRequired, Optional
from langgraph.graph import Graph, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import pandas as pd
import logging
from datetime import datetime, timedelta
from core.agents.function_call_agent import function_call_agent
from core.tools.finance_market_sentiment_analyse import analyze_market_sentiment
from core.tools.strategy_generation import generate_strategy
from core.tools.backtest import quant_analysis
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add constant definitions at the beginning of the file
MAX_STRATEGY_ATTEMPTS = 3

def safe_serialize(obj):
    """Safely serialize objects as primitive types"""
    print('safe_serialize Debug Content:', obj)
    
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif hasattr(obj, 'to_dict'):
        try:
            return obj.to_dict()
        except Exception as e:
            print(f"to_dict Conversion failed: {str(e)}")
            return str(obj)
    elif hasattr(obj, 'to_json'):
        try:
            return obj.to_json()
        except Exception as e:
            print(f"to_json Conversion failed: {str(e)}")
            return str(obj)
    elif isinstance(obj, (list, dict, str, int, float, bool)) or obj is None:
        return obj
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        print(f"Unserializable types: {type(obj)}")
        return str(obj)

class WorkflowState(TypedDict, total=False):
    """Shared state of quantitative trading workflow"""

    # === Input Message ===
    messages: Annotated[Sequence[BaseMessage], "Conversation history"]

    # === Asset metadata information ===
    symbol:     Annotated[str, "For example, AAPL or BTC-USD"]

    # === Backtest related ===
    trading_strategy:  NotRequired[Dict[str, Any]]            
    quant_analysis:  NotRequired[Dict[str, Any]]       

    # === Market sentiment ===
    sentiment_analysis: NotRequired[Dict[str, Any]]

    # === Final report ===
    final_report:      NotRequired[str]

    # === Strategy generation attempts ===
    strategy_attempts: Annotated[int, "Number of strategy generation attempts"]

def create_workflow_graph() -> Graph:
    """Create workflow graph"""
    # Create workflow graph
    workflow = StateGraph(WorkflowState)
    
    # Define nodes
    workflow.add_node("generate_trading_strategy", generate_trading_strategy_node)
    workflow.add_node("run_quant_analysis", quant_analysis_node)
    workflow.add_node("analyze_market_sentiment", analyze_market_sentiment_node)
    workflow.add_node("generate_final_report", generate_final_report_node)
    
    # Define edges
    workflow.add_edge("generate_trading_strategy", "run_quant_analysis")
    workflow.add_conditional_edges(
        "run_quant_analysis",
        lambda x: (
            "generate_trading_strategy" 
            if not x.get("quant_analysis", {}).get("is_satisfactory", False) and x.get("strategy_attempts", 0) < MAX_STRATEGY_ATTEMPTS
            else "analyze_market_sentiment"
        ),
        {
            "generate_trading_strategy": "generate_trading_strategy",
            "analyze_market_sentiment": "analyze_market_sentiment"
        }
    )
    workflow.add_edge("analyze_market_sentiment", "generate_final_report")
    
    # Set entry and exit points
    workflow.set_entry_point("generate_trading_strategy")
    workflow.set_finish_point("generate_final_report")
    
    return workflow.compile()

# Node function definitions

def generate_trading_strategy_node(state: WorkflowState) -> WorkflowState:
    """Generate trading strategy node"""
    try:
        logger.info("Generating trading strategy")
               
        # Check necessary state
        if state.get('symbol') is None:
            logger.error("Asset code not obtained")
            raise ValueError("Asset code not obtained")           
        
        # directly call generate_strategy function
        strategy = generate_strategy()
        
        if strategy is None:
            logger.error("Generating trading strategy failed")
            raise ValueError("Generating trading strategy failed")
            
        # Update state
        state['trading_strategy'] = strategy
        logger.info("Trading strategy generated")
        logger.info(f"Trading strategy content: {json.dumps(strategy, indent=2, ensure_ascii=False)}")

        # Increase the number of attempts
        state['strategy_attempts'] = state.get('strategy_attempts', 0) + 1
        
        return state
    except Exception as e:
        logger.error(f"Generating trading strategy error: {str(e)}")
        raise

def quant_analysis_node(state: WorkflowState) -> WorkflowState:
    """Run quantitative analysis"""
    try:
        logger.info("Running quantitative analysis")
        
        # check necessary state
        if state.get('symbol') is None:
            logger.error("Asset code not obtained")
            raise ValueError("Asset code not obtained")
        if state.get('trading_strategy') is None:
            logger.error("Trading strategy not obtained")
            raise ValueError("Trading strategy not obtained")           
        # directly call quant_analysis function
        result = quant_analysis(
            symbol=state["symbol"],
            strategy=state["trading_strategy"]
        )
        
        if result is None:
            logger.error("Quantitative analysis failed")
            raise ValueError("Quantitative analysis failed")
            
        # update state
        state['quant_analysis'] = result
        logger.info("Quantitative analysis completed")
        
        return state
    except Exception as e:
        logger.error(f"Quantitative analysis error: {str(e)}")
        raise

def analyze_market_sentiment_node(state: WorkflowState) -> WorkflowState:
    """Analyze market sentiment node"""
    try:
        logger.info("Running market sentiment analysis")
        
        # Check necessary state
        if state.get('symbol') is None:
            logger.error("Asset code not obtained")
            raise ValueError("Asset code not obtained")
        # Run market sentiment analysis
        task = f"Please perform market sentiment analysis based on the asset code {state['symbol']}"
        sentiment_analysis = analyze_market_sentiment(state['symbol'])
        
        if sentiment_analysis is None:
            logger.error("Market sentiment analysis failed")
            raise ValueError("Market sentiment analysis failed")
            
        # Update state
        state['sentiment_analysis'] = safe_serialize(sentiment_analysis)
        logger.info("Market sentiment analysis completed")
        
        return state
    except Exception as e:
        logger.error(f"Market sentiment analysis error: {str(e)}")
        raise

def generate_final_report_node(state: WorkflowState) -> WorkflowState:
    """Generate final report node"""
    try:
        logger.info("Generating final report")
        
        # Check necessary state
        if state.get('sentiment_analysis') is None:
            logger.error("Market sentiment analysis result not obtained")
            raise ValueError("Market sentiment analysis result not obtained")
        if state.get('quant_analysis') is None:
            logger.error("Quantitative analysis result not obtained")
            raise ValueError("Quantitative analysis result not obtained")
        
        # Generate final report
        # Import and directly call the generate_report tool
        from core.tools.final_report_generation import ReportAgent
        
        # Parse sentiment_analysis if it's a string (handle incorrect format)
        sentiment_data = state['sentiment_analysis']
        if isinstance(sentiment_data, str):
            # Create a fallback sentiment data structure
            sentiment_data = {
                "overall_sentiment": "neutral",
                "sentiment_score": 0.0,
                "confidence": 0.8,
                "error": "Sentiment analysis format issue",
                "raw_data": sentiment_data
            }
        
        # Create ReportAgent and generate complete report
        report_agent = ReportAgent()
        final_report = report_agent.generate_report(
            quant_analysis_result=state['quant_analysis'],
            market_sentiment_result=sentiment_data
        )
        
        if final_report is None:
            logger.error("Generating final report failed")
            raise ValueError("Generating final report failed")
        
        # Update state
        state['final_report'] = final_report
        logger.info(f"Final report generated with structure: {list(final_report.keys()) if isinstance(final_report, dict) else type(final_report)}")
        
        return state
    except Exception as e:
        logger.error(f"Generating final report error: {str(e)}")
        raise

if __name__ == "__main__":
    # Create workflow graph instance
    workflow_graph = create_workflow_graph()
    
    # Initialize state
    initial_state = WorkflowState(
        messages=[],
        symbol="",      # Provided by frontend
        trading_strategy=None,
        quant_analysis=None,
        sentiment_analysis=None,
        final_report=None,
        strategy_attempts=0 
    )
    
    # Run workflow
    final_state = workflow_graph.invoke(initial_state) 