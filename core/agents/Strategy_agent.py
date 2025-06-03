"""
指标元数据配置文件
包含所有技术指标的参数空间、字段定义和规则模板
"""

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chat_models.openai import ChatOpenAI
from langchain.agents import tool, Tool, initialize_agent, AgentType
from core.indicators import calculate_indicators, get_historical_data
import json
import textwrap
from datetime import datetime
import logging
import pandas as pd
from typing import Dict, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)

INDICATOR_META = {
    # === 趋势类 =========================================================
    "SMA": {
        "desc": "简单移动平均线",
        "fields": ["SMA"],                                # 生成列名示例: SMA_50
        "param_space": {"period": [10, 20, 50, 100, 200]},
        "rule_templates": [
            "close > SMA",                               # 多头
            "close < SMA"                                # 空头
        ]
    },
    "EMA": {
        "desc": "指数移动平均线，对新价格更敏感",
        "fields": ["EMA"],
        "param_space": {"period": [5, 10, 21, 55, 89]},
        "rule_templates": [
            "EMA > SMA",                                 # 趋势确认
            "EMA_crosses_above_SMA"                      # 金叉
        ]
    },
    "MACD": {
        "desc": "快速与慢速 EMA 之差，判断多空动能",
        "fields": ["MACD", "MACD_SIGNAL", "MACD_HIST"],
        "param_space": {
            "fast":   [8, 12, 20],
            "slow":   [18, 26, 40],
            "signal": [6, 9, 12]
        },
        "rule_templates": [
            "MACD > MACD_SIGNAL",                        # 金叉
            "MACD_crosses_below_MACD_SIGNAL"             # 死叉
        ]
    },
    "ADX": {
        "desc": "趋势强度 (0–100)，>25 视为强趋势",
        "fields": ["ADX"],
        "param_space": {"period": [14, 20, 28]},
        "rule_templates": [
            "ADX > {adx_th}",                            # 趋势过滤
            "ADX < {adx_th}"                             # 趋势减弱
        ]
    },

    # === 震荡 / 反转类 ================================================
    "RSI": {
        "desc": "相对强弱指标，<30 超卖，>70 超买",
        "fields": ["RSI"],
        "param_space": {
            "period":  [7, 14],
            "th_low":  [25, 30, 40],
            "th_high": [60, 70, 80]
        },
        "rule_templates": [
            "RSI < {th_low}",                            # 逢低买
            "RSI > {th_high}"                            # 逢高卖
        ]
    },
    "STOCH": {
        "desc": "随机指标 (KD)，判断超买超卖拐点",
        "fields": ["STOCH_K", "STOCH_D"],
        "param_space": {"k_period":[9,14], "d_period":[3]},
        "rule_templates": [
            "STOCH_K_crosses_above_STOCH_D",             # 看涨
            "STOCH_K_crosses_below_STOCH_D"              # 看跌
        ]
    },

    # === 统计波动 / 通道类 ============================================
    "ATR": {
        "desc": "平均真实波幅，用于止损或波动过滤",
        "fields": ["ATR"],
        "param_space": {"period":[7,14,20]},
        "rule_templates": []
    },
    "BBANDS": {
        "desc": "布林带，±k·σ 通道",
        "fields": ["BB_UPPER", "BB_MIDDLE", "BB_LOWER"],
        "param_space": {"period":[20], "stdev":[2, 2.5]},
        "rule_templates": [
            "close > BB_UPPER",                          # 突破
            "close < BB_LOWER"
        ]
    },
    "DONCHIAN": {
        "desc": "唐奇安通道，高低突破",
        "fields": ["DONCHIAN_HIGH", "DONCHIAN_LOW"],
        "param_space": {"period":[20,55]},
        "rule_templates": [
            "close > DONCHIAN_HIGH",                     # 多头突破
            "close < DONCHIAN_LOW"                       # 空头突破
        ]
    },

    # === 动量 / 变化率 ===============================================
    "ROC": {
        "desc": "Rate of Change，动量百分比",
        "fields": ["ROC"],
        "param_space": {"period":[10,20]},
        "rule_templates": [
            "ROC > {pos_th}",                            # 动量向上
            "ROC < -{neg_th}"
        ]
    },

    # === 成交量 / 市场深度 ===========================================
    "OBV": {
        "desc": "能量潮指标，累积成交量动能",
        "fields": ["OBV"],
        "param_space": {},
        "rule_templates": [
            "OBV_rising_for_3_bars"                      # OBV 3 连升
        ]
    }
}

# 策略配置模式定义
STRAT_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["name", "indicators", "params", "rule"],
        "properties": {
            "name": {"type": "string"},
            "indicators": {"type": "array", "items": {"type": "string"}},
            "params": {"type": "object"},
            "rule": {"type": "string"}
        }
    }
}

def build_prompt(indicator_meta: dict,
                 schema: dict = STRAT_SCHEMA) -> ChatPromptTemplate:
    """
    构建策略生成的提示模板
    
    Args:
        indicator_meta: 指标元数据字典
        schema: 策略配置模式定义
        
    Returns:
        ChatPromptTemplate: 组装好的提示模板
    """
    system_part = textwrap.dedent(f"""
        You are an expert quant trader.
        Design a trading strategies **ONLY** with the indicators below.
        Output must pass the JSON schema, no extra text.

        ## JSON Schema
        {json.dumps(schema, indent=2)}
    """)
    
    user_part = f"### INDICATORS\n{json.dumps(indicator_meta, indent=2, ensure_ascii=False)}"

    return ChatPromptTemplate.from_messages(
        [("system", system_part), ("user", user_part)]
    )

@tool("根据指标元数据，生成一个交易策略（包括规则、指标、参数等）")
def generate_strategy() -> dict:
    """
    生成单个交易策略
    
    Returns:
        dict: 生成的策略，包含name、indicators、params和rule字段
    """
    # 构建提示模板
    prompt = build_prompt(INDICATOR_META, STRAT_SCHEMA)
    
    parser = JsonOutputParser()
    
    # 组合成Chain：Prompt → LLM → JSON解析
    chain = prompt | llm | parser
    
    # 执行Chain生成策略
    spec_list = chain.invoke({})
    return spec_list[0]  # 只返回第一个策略

@tool("根据实盘数据和交易策略，使用LLM生成实盘交易信号")
def generate_live_signal(data: pd.DataFrame, strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    使用LLM生成实盘交易信号
    
    Args:
        data: 实盘数据，包含技术指标
        strategy: 策略配置字典
        
    Returns:
        Dict[str, Any]: 包含交易信号的字典
    """
    try:
        # 获取最新的数据点
        latest_data = data.iloc[-1]
        
        # 构建提示
        prompt = f"""
        你是一个资深量化交易员，请根据以下技术指标数据和交易策略，判断当前应该买入、卖出还是持有：
        
        当前价格: {latest_data['CLOSE']}
        技术指标:
        {json.dumps({indicator: latest_data[indicator] for indicator in strategy['indicators']}, indent=2)}
        
        交易策略:
        {json.dumps(strategy, indent=2, ensure_ascii=False)}
        
        请只回答: BUY, SELL 或 HOLD
        """
        
        # 调用LLM获取信号
        response = llm.invoke(prompt)
        signal = response.strip().upper()
        
        # 验证信号有效性
        if signal not in ["BUY", "SELL", "HOLD"]:
            signal = "HOLD"  # 默认持有
            
        # 返回信号详情
        return signal
        
    except Exception as e:
        logger.error(f"生成交易信号时出错: {str(e)}")
        raise 

# 初始化LLM和解析器
llm = ChatOpenAI(model="gpt-4", temperature=0.2)

def get_tools():
    from core.backtest import backtest_strategy, evaluate_backtest
    return [generate_strategy, backtest_strategy, evaluate_backtest, calculate_indicators, get_historical_data, generate_live_signal]

quant_agent = initialize_agent(
    tools=get_tools(),
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)