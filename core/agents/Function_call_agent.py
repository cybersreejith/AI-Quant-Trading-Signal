from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

def get_function_call_tools():
    from core.tools.backtest import quant_analysis
    from core.tools.finance_market_sentiment_analyse import SentimentAgent
    from core.tools.final_report_generation import ReportAgent
    from core.tools.strategy_generation import generate_strategy
    return [generate_strategy,quant_analysis,SentimentAgent.analyze_market_sentiment,ReportAgent.generate_report]

function_call_agent = initialize_agent(
    tools=get_function_call_tools(),
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)