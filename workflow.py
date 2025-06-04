from typing import TypedDict, Annotated, Sequence, Dict, Any, NotRequired, Optional
from langgraph.graph import Graph, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import pandas as pd
import logging
from core.indicators import calculate_indicators
from core.agents.sentiment_agent import SentimentAgent
from datetime import datetime, timedelta
from core.agents.report_agent import ReportAgent
from core.backtest import evaluate_backtest
from core.agents.Strategy_agent import quant_agent

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
    backtest_results:  NotRequired[Dict[str, Any]]       # 指标 JSON
    backtest_evaluation: NotRequired[Dict[str, Any]]     # AI 评价

    # === 市场情绪 ===
    sentiment_analysis: NotRequired[Dict[str, Any]]

    # === 最终报告 ===
    final_report:      NotRequired[str]

    # === 实时信号 ===
    live_signal:       NotRequired[Dict[str, Any]]

def create_workflow_graph() -> Graph:
    """创建工作流图"""
    # 创建工作流图
    workflow = StateGraph(WorkflowState)
    
    # 定义节点
    workflow.add_node("get_historical_data", get_historical_data_node)
    workflow.add_node("calculate_indicators", calculate_indicators_node)
    workflow.add_node("generate_trading_strategy", generate_trading_strategy_node)
    workflow.add_node("backtest_strategy", backtest_strategy_node)
    workflow.add_node("evaluate_backtest", evaluate_backtest_node)
    workflow.add_node("generate_live_signal", generate_live_signal_node)
    workflow.add_node("analyze_market_sentiment", analyze_market_sentiment_node)
    workflow.add_node("generate_final_report", generate_final_report_node)
    
    # 定义边
    workflow.add_edge("get_historical_data", "calculate_indicators")
    workflow.add_edge("calculate_indicators", "generate_trading_strategy")
    workflow.add_edge("generate_trading_strategy", "backtest_strategy")
    workflow.add_edge("backtest_strategy", "evaluate_backtest")
    workflow.add_conditional_edges(
        "evaluate_backtest",
        lambda x: "generate_trading_strategy" if not x["backtest_evaluation"]["is_satisfactory"] else "generate_live_signal",
        {
            "generate_trading_strategy": "generate_trading_strategy",
            "generate_live_signal": "generate_live_signal"
        }
    )
    workflow.add_edge("generate_live_signal", "analyze_market_sentiment")
    workflow.add_edge("analyze_market_sentiment", "generate_final_report")
    
    # 设置入口和出口
    workflow.set_entry_point("get_historical_data")
    workflow.set_finish_point("generate_final_report")
    
    return workflow.compile()

# 节点函数定义
def get_historical_data_node(state: WorkflowState) -> WorkflowState:
    """获取历史数据节点"""
    try:
        logger.info("获取历史数据")
        print("=== 开始获取历史数据 ===")
        
        # 检查必要的状态
        if not state.get('symbol'):
            logger.error("未选择资产代码")
            raise ValueError("未选择资产代码")
            
        # 获取历史数据
        task = f"请获取资产 {state['symbol']}的历史行情数据"
        print(f"执行任务: {task}")
        
        try:
            # 使用 invoke 替代 run
            historical_data = quant_agent.invoke({"input": task})
            print("quant_agent.invoke 返回类型:", type(historical_data))
            print("quant_agent.invoke 返回内容:", historical_data)
        except Exception as e:
            print(f"quant_agent.invoke 执行出错: {str(e)}")
            raise
        
        if historical_data is None:
            logger.error(f"获取 {state['symbol']} 的历史数据失败")
            raise ValueError(f"获取 {state['symbol']} 的历史数据失败")
            
        # 更新状态 - 确保数据可序列化
        if isinstance(historical_data, pd.DataFrame):
            print("转换 DataFrame 为 dict")
            state['historical_data'] = historical_data.to_dict(orient='records')
        else:
            print("使用 safe_serialize 处理数据")
            state['historical_data'] = safe_serialize(historical_data)
            
        logger.info(f"成功获取 {state['symbol']} 的历史数据")
        print("=== 历史数据获取完成 ===")
        
        return state
    except Exception as e:
        logger.error(f"获取历史数据时出错: {str(e)}")
        print(f"获取历史数据时出错: {str(e)}")
        raise

def calculate_indicators_node(state: WorkflowState) -> WorkflowState:
    """计算技术指标节点"""
    try:
        logger.info("计算技术指标")
        
        # 检查必要的状态
        if state.get('historical_data') is None:
            logger.error("未获取历史数据")
            raise ValueError("未获取历史数据")           
        # 计算技术指标
        task = f"请计算资产 {state['historical_data']}的技术指标"
        technical_data = quant_agent.run(task)
        
        if technical_data is None:
            logger.error("计算技术指标失败")
            raise ValueError("计算技术指标失败")
            
        # 更新状态
        state['technical_data'] = safe_serialize(technical_data)
        logger.info("技术指标计算完成")
        
        return state
    except Exception as e:
        logger.error(f"计算技术指标时出错: {str(e)}")
        raise


def generate_trading_strategy_node(state: WorkflowState) -> WorkflowState:
    """生成交易策略节点"""
    try:
        logger.info("生成交易策略")
        
        # 检查必要的状态
        if state.get('technical_data') is None:
            logger.error("未获取技术指标")
            raise ValueError("未获取技术指标")           
        # 生成交易策略
        task = f"请生成资产 {state['symbol']}的交易策略"
        trading_strategy = quant_agent.run(task)
        
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

def backtest_strategy_node(state: WorkflowState) -> WorkflowState:
    """运行回测节点"""
    try:
        logger.info("运行回测")
        
        # 检查必要的状态
        if state.get('trading_strategy') is None:
            logger.error("未获取交易策略")
            raise ValueError("未获取交易策略")
        if state.get('technical_data') is None:
            logger.error("未获取技术指标")
            raise ValueError("未获取技术指标")  
        # 运行回测
        task = f"请根据资产技术指标数据 {state['technical_data']} 和交易策略 {state['trading_strategy']} 进行回测"
        backtest_results = quant_agent.run(task)
        
        if backtest_results is None:
            logger.error("回测失败")
            raise ValueError("回测失败")
            
        # 更新状态
        state['backtest_results'] = safe_serialize(backtest_results)
        logger.info("回测完成")
        
        return state
    except Exception as e:
        logger.error(f"回测时出错: {str(e)}")
        raise

def evaluate_backtest_node(state: WorkflowState) -> WorkflowState:
    """评估回测结果节点"""
    try:
        logger.info("评估回测结果")
        
        # 检查必要数据
        if state.get('backtest_results') is None:
            logger.error("未获取回测结果")
            raise ValueError("未获取回测结果")
        # 使用quant_agent.run评估回测结果
        task = f"请根据回测结果 {state['backtest_results']} 进行评估"
        evaluation = quant_agent.run(task)
        if evaluation is None:
            logger.error("评估回测结果失败")
            raise ValueError("评估回测结果失败")
        # 更新状态
        print('evaluate_backtest_node 调用 safe_serialize 前 evaluation 类型:', type(evaluation))
        print('evaluate_backtest_node 调用 safe_serialize 前 evaluation 内容:', evaluation)
        state['backtest_evaluation'] = safe_serialize(evaluation)
        logger.info("回测评估完成")
        return state
    except Exception as e:
        logger.error(f"评估回测结果时出错: {str(e)}")
        raise

def generate_live_signal_node(state: WorkflowState) -> WorkflowState:
    """生成实时交易信号节点"""
    try:
        logger.info("生成实时交易信号")
        
        # 检查必要数据
        if state.get('trading_strategy') is None:
            logger.error("未获取交易策略")
            raise ValueError("未获取交易策略")
        if state.get('technical_data') is None:
            logger.error("未获取技术指标")
            raise ValueError("未获取技术指标")
        # 生成实时交易信号
        task = f"请根据资产技术指标数据 {state['technical_data']} 和交易策略 {state['trading_strategy']} 生成实时交易信号"
        live_signal = quant_agent.run(task)
        if live_signal is None:
            logger.error("生成实时交易信号失败")
            raise ValueError("生成实时交易信号失败")
        # 更新状态
        state['live_signal'] = safe_serialize(live_signal)
        logger.info(f"实时交易信号生成完成: {live_signal}")
        return state
    except Exception as e:
        logger.error(f"生成实时交易信号时出错: {str(e)}")
        raise

def analyze_market_sentiment_node(state: WorkflowState) -> WorkflowState:
    """分析市场情绪节点"""
    try:
        logger.info("开始分析市场情绪")
        
        # 检查必要数据
        if not state.get('symbol'):
            logger.error("未设置资产代码")
            raise ValueError("未设置资产代码")
            
        # 初始化情绪分析agent
        sentiment_agent = SentimentAgent()
        
        # 分析市场情绪
        sentiment_result = sentiment_agent.analyze_market_sentiment(state['symbol'])
        
        # 更新状态
        state['sentiment_analysis'] = safe_serialize(sentiment_result)
        logger.info(f"市场情绪分析完成: {sentiment_result}")
        
        return state
        
    except Exception as e:
        logger.error(f"分析市场情绪时出错: {str(e)}")
        raise

def generate_final_report_node(state: WorkflowState) -> WorkflowState:
    """生成最终报告节点"""
    try:
        logger.info("开始生成最终报告")
        
        # 检查必要数据
        required_data = ["backtest_results", "live_signal", "sentiment_analysis"]
        missing_data = [field for field in required_data if field not in state]
        
        if missing_data:
            logger.error(f"缺少必要数据: {', '.join(missing_data)}")
            raise ValueError(f"缺少必要数据: {', '.join(missing_data)}")
            
        # 初始化报告生成agent
        report_agent = ReportAgent()
        
        # 准备分析数据
        analysis_data = {
            "backtest_results": state["backtest_results"],
            "live_signal": state["live_signal"],
            "sentiment_analysis": state["sentiment_analysis"]
        }
        
        # 生成报告
        report = report_agent.generate_report(analysis_data)
        
        if "error" in report:
            logger.error(f"生成报告失败: {report['error']}")
            raise ValueError(f"生成报告失败: {report['error']}")
            
        # 更新工作流状态
        state["final_report"] = report
        
        logger.info("最终报告生成完成")
        return state
        
    except Exception as e:
        logger.error(f"生成最终报告时出错: {str(e)}")
        raise

if __name__ == "__main__":
    # 创建工作流图实例
    workflow_graph = create_workflow_graph()
    
    # 初始化状态
    initial_state = WorkflowState(
        messages=[],
        symbol="",      # 由前端传入
        historical_data=None,
        technical_data=None,
        trading_strategy=None,
        backtest_results=None,
        backtest_evaluation={"is_satisfactory": False},
        sentiment_analysis=None,
        final_report="",
        live_signal=None
    )
    
    # 运行工作流
    final_state = workflow_graph.invoke(initial_state) 