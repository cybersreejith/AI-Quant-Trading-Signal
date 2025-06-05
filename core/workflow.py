from typing import TypedDict, Annotated, Sequence, Dict, Any, NotRequired, Optional
from langgraph.graph import Graph, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import pandas as pd
import logging
from datetime import datetime, timedelta
from core.agents.Function_call_agent import function_call_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_serialize(obj):
    """安全序列化对象为基本类型"""
    print('safe_serialize 调试类型:', type(obj))
    print('safe_serialize 调试内容:', obj)
    
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif hasattr(obj, 'to_dict'):
        try:
            return obj.to_dict()
        except Exception as e:
            print(f"to_dict 转换失败: {str(e)}")
            return str(obj)
    elif hasattr(obj, 'to_json'):
        try:
            return obj.to_json()
        except Exception as e:
            print(f"to_json 转换失败: {str(e)}")
            return str(obj)
    elif isinstance(obj, (list, dict, str, int, float, bool)) or obj is None:
        return obj
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        print(f"无法序列化的类型: {type(obj)}")
        return str(obj)

class WorkflowState(TypedDict, total=False):
    """量化交易工作流的共享状态"""

    # === 输入消息 ===
    messages: Annotated[Sequence[BaseMessage], "对话历史"]

    # === 资产元信息 ===
    symbol:     Annotated[str, "例如 AAPL 或 BTC-USD"]

    # === 历史行情 ===
    historical_data:   NotRequired[Dict[str, Any]]         # OHLCV
    technical_data:    NotRequired[Dict[str, Any]]         # 含指标的 DF

    # === 回测相关 ===
    trading_strategy:  NotRequired[Dict[str, Any]]                  # backtrader.Strategy
    quant_analysis_results:  NotRequired[Dict[str, Any]]       # 指标 JSON

    # === 市场情绪 ===
    sentiment_analysis: NotRequired[Dict[str, Any]]

    # === 最终报告 ===
    final_report:      NotRequired[str]

def create_workflow_graph() -> Graph:
    """创建工作流图"""
    # 创建工作流图
    workflow = StateGraph(WorkflowState)
    
    # 定义节点
    workflow.add_node("generate_trading_strategy", generate_trading_strategy_node)
    workflow.add_node("quant_analysis", quant_analysis_node)
    workflow.add_node("analyze_market_sentiment", analyze_market_sentiment_node)
    workflow.add_node("generate_final_report", generate_final_report_node)
    
    # 定义边
    workflow.add_edge("generate_trading_strategy", "quant_analysis")
    workflow.add_conditional_edges(
        "quant_analysis",
        lambda x: "generate_trading_strategy" if not x["quant_analysis"]["is_satisfactory"] else "analyze_market_sentiment",
        {
            "generate_trading_strategy": "generate_trading_strategy",
            "analyze_market_sentiment": "analyze_market_sentiment"
        }
    )
    workflow.add_edge("analyze_market_sentiment", "generate_final_report")
    
    # 设置入口和出口
    workflow.set_entry_point("generate_trading_strategy")
    workflow.set_finish_point("generate_final_report")
    
    return workflow.compile()

# 节点函数定义

def generate_trading_strategy_node(state: WorkflowState) -> WorkflowState:
    """生成交易策略节点"""
    try:
        logger.info("生成交易策略")
        
        # 检查必要的状态
        if state.get('symbol') is None:
            logger.error("未获取资产代码")
            raise ValueError("未获取资产代码")           
        # 生成交易策略
        task = f"请生成一个资产 {state['symbol']}的交易策略"
        trading_strategy = function_call_agent.run(task)
        
        if trading_strategy is None:
            logger.error("生成交易策略失败")
            raise ValueError("生成交易策略失败")
            
        # 更新状态
        state['trading_strategy'] = safe_serialize(trading_strategy)
        logger.info("交易策略生成完成")
        
        return state
    except Exception as e:
        logger.error(f"生成交易策略时出错: {str(e)}")
        raise    

def quant_analysis_node(state: WorkflowState) -> WorkflowState:
    """量化分析节点"""
    try:
        logger.info("运行量化分析")
        
        # 检查必要的状态
        if state.get('symbol') is None:
            logger.error("未获取资产代码")
            raise ValueError("未获取资产代码")
        if state.get('trading_strategy') is None:
            logger.error("未获取交易策略")
            raise ValueError("未获取交易策略")  
        # 运行回测
        task = f"请根据资产代码 {state['symbol']} 和交易策略 {state['trading_strategy']} 进行量化分析"
        quant_analysis_results = function_call_agent.run(task)
        
        if quant_analysis_results is None:
            logger.error("量化分析失败")
            raise ValueError("量化分析失败")
            
        # 更新状态
        state['quant_analysis_results'] = safe_serialize(quant_analysis_results)
        logger.info("量化分析完成")
        
        return state
    except Exception as e:
        logger.error(f"量化分析时出错: {str(e)}")
        raise




def analyze_market_sentiment_node(state: WorkflowState) -> WorkflowState:
    """分析市场情绪节点"""
    


def generate_final_report_node(state: WorkflowState) -> WorkflowState:
    """生成最终报告节点"""


if __name__ == "__main__":
    # 创建工作流图实例
    workflow_graph = create_workflow_graph()
    
    # 初始化状态
    initial_state = WorkflowState(
        messages=[],
        symbol="",      # 由前端传入
        trading_strategy=None,
        quant_analysis_results=None,
        sentiment_analysis=None,
        final_report="",
    )
    
    # 运行工作流
    final_state = workflow_graph.invoke(initial_state) 