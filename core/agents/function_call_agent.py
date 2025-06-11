from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

def get_function_call_tools():
    from core.tools.finance_market_sentiment_analyse import analyze_market_sentiment
    from core.tools.final_report_generation import generate_report
    return [analyze_market_sentiment, generate_report]


# 初始化 agent
function_call_agent = initialize_agent(
    tools=get_function_call_tools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)