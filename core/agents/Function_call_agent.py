from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

def get_function_call_tools():
    from core.tools.Backtest import quant_analysis
    from core.tools.Finance_market_sentiment_analyse import analyze_market_sentiment
    from core.tools.Final_report_generation import generate_report
    from core.tools.Strategy_generation import generate_strategy
    return [generate_strategy,quant_analysis,analyze_market_sentiment,generate_report]

function_call_agent = initialize_agent(
    tools=get_function_call_tools(),
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)