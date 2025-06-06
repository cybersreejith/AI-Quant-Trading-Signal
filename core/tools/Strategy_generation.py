"""
Indicator metadata configuration file
Contains all technical indicator parameter spaces, field definitions, and rule templates
"""

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chat_models.openai import ChatOpenAI
from langchain.agents import tool
import json
import textwrap
from typing import Dict, Any
from utils.logger import setup_logger
from config.settings import STRAT_SCHEMA, INDICATOR_META

logger = setup_logger(__name__)

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
@tool("Generate a quantitative trading strategy")
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

# Initialize LLM and parser
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)   

