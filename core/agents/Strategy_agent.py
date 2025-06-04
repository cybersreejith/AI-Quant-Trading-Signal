"""
Indicator metadata configuration file
Contains all technical indicator parameter spaces, field definitions, and rule templates
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
    # === Trend class =========================================================
    "SMA": {
        "desc": "Simple Moving Average",
        "fields": ["SMA"],                                # Example of generating column names: SMA_50
        "param_space": {"period": [10, 20, 50, 100, 200]},
        "rule_templates": [
            "close > SMA",                               # Bullish
            "close < SMA"                                # Bearish
        ]
    },
    "EMA": {
        "desc": "Exponential Moving Average, more sensitive to new prices",
        "fields": ["EMA"],
        "param_space": {"period": [5, 10, 21, 55, 89]},
        "rule_templates": [
            "EMA > SMA",                                 # Trend confirmation
            "EMA_crosses_above_SMA"                      # Golden cross
        ]
    },
    "MACD": {
        "desc": "The difference between the fast and slow EMA, to judge the bullish and bearish momentum",
        "fields": ["MACD", "MACD_SIGNAL", "MACD_HIST"],
        "param_space": {
            "fast":   [8, 12, 20],
            "slow":   [18, 26, 40],
            "signal": [6, 9, 12]
        },
        "rule_templates": [
            "MACD > MACD_SIGNAL",                        # Golden cross
            "MACD_crosses_below_MACD_SIGNAL"             # Dead cross
        ]
    },
    "ADX": {
        "desc": "Trend strength (0–100), >25 is considered a strong trend",
        "fields": ["ADX"],
        "param_space": {"period": [14, 20, 28]},
        "rule_templates": [
            "ADX > {adx_th}",                            # Trend filtering
            "ADX < {adx_th}"                             # Trend weakening
        ]
    },

    # === Oscillation / Reversal class ================================================
    "RSI": {
        "desc": "Relative Strength Index, <30 is oversold, >70 is overbought",
        "fields": ["RSI"],
        "param_space": {
            "period":  [7, 14],
            "th_low":  [25, 30, 40],
            "th_high": [60, 70, 80]
        },
        "rule_templates": [
            "RSI < {th_low}",                            # Buy at low
            "RSI > {th_high}"                            # Sell at high
        ]
    },
    "STOCH": {
        "desc": "Stochastic indicator (KD), to judge the oversold and overbought points",
        "fields": ["STOCH_K", "STOCH_D"],
        "param_space": {"k_period":[9,14], "d_period":[3]},
        "rule_templates": [
            "STOCH_K_crosses_above_STOCH_D",             # Bullish
            "STOCH_K_crosses_below_STOCH_D"              # Bearish
        ]
    },

    # === Statistical volatility / Channel class ============================================
    "ATR": {
        "desc": "Average True Range, used for stop loss or volatility filtering",
        "fields": ["ATR"],
        "param_space": {"period":[7,14,20]},
        "rule_templates": []
    },
    "BBANDS": {
        "desc": "Bollinger Bands, ±k·σ channel",
        "fields": ["BB_UPPER", "BB_MIDDLE", "BB_LOWER"],
        "param_space": {"period":[20], "stdev":[2, 2.5]},
        "rule_templates": [
            "close > BB_UPPER",                          # Breakout
            "close < BB_LOWER"
        ]
    },
    "DONCHIAN": {
        "desc": "Donchian Channel, high and low breakout",
        "fields": ["DONCHIAN_HIGH", "DONCHIAN_LOW"],
        "param_space": {"period":[20,55]},
        "rule_templates": [
            "close > DONCHIAN_HIGH",                     # Bullish breakout
            "close < DONCHIAN_LOW"                       # Bearish breakout
        ]
    },

    # === Momentum / Rate of change ===============================================
    "ROC": {
        "desc": "Rate of Change, momentum percentage",
        "fields": ["ROC"],
        "param_space": {"period":[10,20]},
        "rule_templates": [
            "ROC > {pos_th}",                            # Momentum up
            "ROC < -{neg_th}"
        ]
    },

    # === Volume / Market depth ===========================================
    "OBV": {
        "desc": "On Balance Volume, cumulative volume momentum",
        "fields": ["OBV"],
        "param_space": {},
        "rule_templates": [
            "OBV_rising_for_3_bars"                      # OBV 3 consecutive rises
        ]
    }
}

# Strategy configuration schema definition
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
    Build the prompt template for strategy generation
    
    Args:
        indicator_meta: The dictionary of indicator metadata
        schema: The definition of strategy configuration schema
        
    Returns:
        ChatPromptTemplate: The assembled prompt template
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

@tool("Generate a trading strategy based on indicator metadata (including rules, indicators, parameters, etc.)")
def generate_strategy() -> dict:
    """
    Generate a single trading strategy
    
    Returns:
        dict: The generated strategy, containing the name, indicators, params, and rule fields
    """
    # Build prompt template
    prompt = build_prompt(INDICATOR_META, STRAT_SCHEMA)
    
    parser = JsonOutputParser()
    
    # Combine into Chain: Prompt → LLM → JSON parsing
    chain = prompt | llm | parser
    
    # Execute Chain to generate strategy
    spec_list = chain.invoke({})
    return spec_list[0]  # Only return the first strategy

@tool("Generate a live trading signal using LLM based on live data and trading strategy")
def generate_live_signal(data: pd.DataFrame, strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a live trading signal using LLM based on live data and trading strategy
    
    Args:
        data: Live data, containing technical indicators
        strategy: Strategy configuration dictionary
        
    Returns:
        Dict[str, Any]: The dictionary containing the trading signal
    """
    try:
        # Get the latest data point
        latest_data = data.iloc[-1]
        
        # Build prompt
        prompt = f"""
        You are an expert quant trader.
        Please determine whether to buy, sell, or hold based on the following technical indicator data and trading strategy:
        
        Current price: {latest_data['CLOSE']}
        Technical indicators:
        {json.dumps({indicator: latest_data[indicator] for indicator in strategy['indicators']}, indent=2)}
        
        Trading strategy:
        {json.dumps(strategy, indent=2, ensure_ascii=False)}
        
        Please only answer: BUY, SELL or HOLD
        """
        
        # Call LLM to get signal
        response = llm.invoke(prompt)
        signal = response.strip().upper()
        
        # Validate signal validity
        if signal not in ["BUY", "SELL", "HOLD"]:
            signal = "HOLD"  # Default hold
            
        # Return signal details
        return signal
        
    except Exception as e:
        logger.error(f"Error generating trading signal: {str(e)}")
        raise 

# Initialize LLM and parser
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