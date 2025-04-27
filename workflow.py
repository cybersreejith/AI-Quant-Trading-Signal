from typing import TypedDict, Annotated, Sequence, Dict, Any, NotRequired, Optional
from langgraph.graph import Graph, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import pandas as pd
import logging
from AI_Quant_Trading import (
    select_asset_type_menu,
    display_asset_reference_list,
    input_asset_symbol,
    get_date_range,
    get_historical_data
)
from core.indicators import calculate_indicators

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowState(TypedDict, total=False):
    """量化交易工作流的共享状态"""

    # === 输入消息 ===
    messages: Annotated[Sequence[BaseMessage], "对话历史"]

    # === 资产元信息 ===
    asset_type: Annotated[str, "股票 / ETF / 外汇 / 加密货币"]
    symbol:     Annotated[str, "例如 AAPL 或 BTC-USD"]
    start_date: Annotated[str, "回测开始日期"]
    end_date:   Annotated[str, "回测结束日期"]

    # === 历史行情 ===
    historical_data:   NotRequired[pd.DataFrame]         # OHLCV
    technical_data:    NotRequired[pd.DataFrame]         # 含指标的 DF

    # === 回测相关 ===
    backtest_dataset:  NotRequired[pd.DataFrame]
    trading_strategy:  NotRequired[Any]                  # backtrader.Strategy
    backtest_results:  NotRequired[Dict[str, Any]]       # 指标 JSON
    backtest_evaluation: NotRequired[Dict[str, Any]]     # AI 评价

    # === 市场情绪 ===
    sentiment_analysis: NotRequired[Dict[str, Any]]

    # === 最终报告 ===
    final_report:      NotRequired[str]

def create_workflow_graph() -> Graph:
    """创建工作流图"""
    # 创建工作流图
    workflow = StateGraph(WorkflowState)
    
    # 定义节点
    workflow.add_node("select_asset_type", select_asset_type_node)
    workflow.add_node("display_reference_list", display_reference_list_node)
    workflow.add_node("input_symbol", input_symbol_node)
    workflow.add_node("get_date_range", get_date_range_node)
    workflow.add_node("get_historical_data", get_historical_data_node)
    workflow.add_node("calculate_indicators", calculate_indicators_node)
    workflow.add_node("prepare_backtest_data", prepare_backtest_data_node)
    workflow.add_node("generate_trading_strategy", generate_trading_strategy_node)
    workflow.add_node("run_backtest", run_backtest_node)
    workflow.add_node("evaluate_backtest", evaluate_backtest_node)
    workflow.add_node("analyze_market_sentiment", analyze_market_sentiment_node)
    workflow.add_node("generate_final_report", generate_final_report_node)
    
    # 定义边
    workflow.add_edge("select_asset_type", "display_reference_list")
    workflow.add_edge("display_reference_list", "input_symbol")
    workflow.add_edge("input_symbol", "get_date_range")
    workflow.add_edge("get_date_range", "get_historical_data")
    workflow.add_edge("get_historical_data", "calculate_indicators")
    workflow.add_edge("calculate_indicators", "prepare_backtest_data")
    workflow.add_edge("prepare_backtest_data", "generate_trading_strategy")
    workflow.add_edge("generate_trading_strategy", "run_backtest")
    workflow.add_edge("run_backtest", "evaluate_backtest")
    workflow.add_conditional_edges(
        "evaluate_backtest",
        lambda x: "generate_trading_strategy" if not x["backtest_evaluation"]["is_satisfactory"] else "analyze_market_sentiment",
        {
            "generate_trading_strategy": "generate_trading_strategy",
            "analyze_market_sentiment": "analyze_market_sentiment"
        }
    )
    workflow.add_edge("analyze_market_sentiment", "generate_final_report")
    
    # 设置入口和出口
    workflow.set_entry_point("select_asset_type")
    workflow.set_finish_point("generate_final_report")
    
    return workflow.compile()

# 节点函数定义
def select_asset_type_node(state: WorkflowState) -> WorkflowState:
    """资产类型选择节点"""
    try:
        logger.info("选择资产类型")
        
        # 调用资产类型选择菜单
        choice = select_asset_type_menu()
        
        # 如果用户选择退出
        if choice is None:
            logger.info("用户选择退出")
            return state
            
        # 将选择转换为资产类型
        asset_types = {
            '1': '股票',
            '2': 'ETF',
            '3': '外汇',
            '4': '加密货币'
        }
        
        # 更新状态
        state['asset_type'] = asset_types[choice]
        logger.info(f"选择的资产类型: {state['asset_type']}")
        
        return state
    except Exception as e:
        logger.error(f"选择资产类型时出错: {str(e)}")
        raise

def display_reference_list_node(state: WorkflowState) -> WorkflowState:
    """显示参考列表节点"""
    try:
        logger.info("显示参考列表")
        
        # 检查资产类型是否已选择
        if not state.get('asset_type'):
            logger.error("未选择资产类型")
            raise ValueError("未选择资产类型")
            
        # 调用显示参考列表函数
        display_asset_reference_list(state['asset_type'])
        
        return state
    except Exception as e:
        logger.error(f"显示参考列表时出错: {str(e)}")
        raise

def input_symbol_node(state: WorkflowState) -> WorkflowState:
    """输入资产代码节点"""
    try:
        logger.info("输入资产代码")
        
        # 调用资产代码输入函数
        symbol = input_asset_symbol()
        
        # 如果用户未输入资产代码
        if symbol is None:
            logger.info("用户未输入资产代码")
            return state
            
        # 更新状态
        state['symbol'] = symbol
        logger.info(f"输入的资产代码: {state['symbol']}")
        
        return state
    except Exception as e:
        logger.error(f"输入资产代码时出错: {str(e)}")
        raise

def get_date_range_node(state: WorkflowState) -> WorkflowState:
    """获取日期范围节点"""
    try:
        logger.info("获取日期范围")
        
        # 调用日期范围获取函数
        start_date, end_date = get_date_range()
        
        # 更新状态
        state['start_date'] = start_date
        state['end_date'] = end_date
        logger.info(f"日期范围: {start_date} 至 {end_date}")
        
        return state
    except Exception as e:
        logger.error(f"获取日期范围时出错: {str(e)}")
        raise

def get_historical_data_node(state: WorkflowState) -> WorkflowState:
    """获取历史数据节点"""
    try:
        logger.info("获取历史数据")
        
        # 检查必要的状态
        if not state.get('symbol'):
            logger.error("未选择资产代码")
            raise ValueError("未选择资产代码")
            
        # 获取历史数据
        df = get_historical_data(
            symbol=state['symbol'],
            start_date=state.get('start_date'),
            end_date=state.get('end_date')
        )
        
        if df is None:
            logger.error(f"获取 {state['symbol']} 的历史数据失败")
            raise ValueError(f"获取 {state['symbol']} 的历史数据失败")
            
        # 更新状态
        state['historical_data'] = df
        logger.info(f"成功获取 {state['symbol']} 的历史数据，数据形状: {df.shape}")
        
        return state
    except Exception as e:
        logger.error(f"获取历史数据时出错: {str(e)}")
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
        df = calculate_indicators(state['historical_data'])
        
        if df is None:
            logger.error("计算技术指标失败")
            raise ValueError("计算技术指标失败")
            
        # 更新状态
        state['technical_data'] = df
        logger.info(f"技术指标计算完成，数据形状: {df.shape}")
        
        return state
    except Exception as e:
        logger.error(f"计算技术指标时出错: {str(e)}")
        raise

def prepare_backtest_data_node(state: WorkflowState) -> WorkflowState:
    """准备回测数据集节点"""
    try:
        # TODO: 实现回测数据集准备逻辑
        logger.info("准备回测数据集")
        return state
    except Exception as e:
        logger.error(f"准备回测数据集时出错: {str(e)}")
        raise

def generate_trading_strategy_node(state: WorkflowState) -> WorkflowState:
    """生成交易策略节点"""
    try:
        # TODO: 实现交易策略生成逻辑
        logger.info("生成交易策略")
        return state
    except Exception as e:
        logger.error(f"生成交易策略时出错: {str(e)}")
        raise

def run_backtest_node(state: WorkflowState) -> WorkflowState:
    """运行回测节点"""
    try:
        # TODO: 实现回测运行逻辑
        logger.info("运行回测")
        return state
    except Exception as e:
        logger.error(f"运行回测时出错: {str(e)}")
        raise

def evaluate_backtest_node(state: WorkflowState) -> WorkflowState:
    """评估回测结果节点"""
    try:
        # TODO: 实现回测结果评估逻辑
        logger.info("评估回测结果")
        return state
    except Exception as e:
        logger.error(f"评估回测结果时出错: {str(e)}")
        raise

def analyze_market_sentiment_node(state: WorkflowState) -> WorkflowState:
    """分析市场情绪节点"""
    try:
        # TODO: 实现市场情绪分析逻辑
        logger.info("分析市场情绪")
        return state
    except Exception as e:
        logger.error(f"分析市场情绪时出错: {str(e)}")
        raise

def generate_final_report_node(state: WorkflowState) -> WorkflowState:
    """生成最终报告节点"""
    try:
        # TODO: 实现最终报告生成逻辑
        logger.info("生成最终报告")
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
        asset_type="",
        symbol="",
        start_date="",
        end_date="",
        historical_data=None,
        technical_data=None,
        backtest_dataset=None,
        trading_strategy=None,
        backtest_results=None,
        backtest_evaluation={"is_satisfactory": False},
        sentiment_analysis=None,
        final_report=""
    )
    
    # 运行工作流
    final_state = workflow_graph.invoke(initial_state) 