from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

import sys
 
# adding Folder_2 to the system path
sys.path.insert(0, '../')
 
from common.utils import Utils
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain.agents import tool, initialize_agent, AgentType
import requests
from langchain.agents import AgentExecutor

@tool
def search_tiker_by_stockname(stock_name: str) -> int:
    """
    use this tool to get the ticker of a stock.
    compose the input in the json format
    input requirements:
    stock_name string, such as a company or stock name

    This tool get a stock's ticker, then this ticker could be used in tool get_stock_price_by_tiker
    """

    print("executing search_tiker_by_stockname ...")
    url = "https://api.polygon.io/v3/reference/tickers?market=stocks&search={stock_name}&active=true&sort=name&apiKey=_O899h4QYZQiv8p_nB1bzp4xEs7sUGAV"\
        .format(stock_name=stock_name)
    response = requests.get(url)
    return response.json()

@tool
def get_stock_price_by_tiker(ticker_name: str, timespan: str, from_date:str, to_date:str) -> int:
    """
    use this tool to get the stock price given its ticker.
    compose the input in the json format
    input requirements:
        * 2 input dates, which is a time range from yyyy-MM-dd to yyyy-MM-dd)
        * timespan(options are `day`, `hour`, `week`, `month`, or `year`)
        * tiker name, need to call search_tiker_by_stockname to get tiker name for a stock
    """

    print("executing get_stick_price_by_tiker ...")
    url = "https://api.polygon.io/v2/aggs/ticker/{ticker_name}/range/1/{timespan}/{from_date}/{to_date}?adjusted=true&sort=asc&limit=120&apiKey=_O899h4QYZQiv8p_nB1bzp4xEs7sUGAV"\
        .format(ticker_name=ticker_name, timespan=timespan, from_date=from_date, to_date=to_date)
    response = requests.get(url)
    return response.json()

tools = [search_tiker_by_stockname, get_stock_price_by_tiker]

llm = ChatOpenAI(openai_api_key = Utils.get_openai_key(), temperature=0, model='gpt-3.5-turbo-0613', streaming=True)
set_llm_cache(InMemoryCache())

#from langchain.tools.render import format_tool_to_openai_function
#llm_with_tools = chatOpenAI.bind(
#    functions=[format_tool_to_openai_function(t) for t in tools]
#)


#agent_executor = initialize_agent(
#    tools,
#    llm,
#    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#    verbose=True,
#)
agent_executor = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

agent_executor.run("what is the average stock close price of DBS on 2023-09-28?")
#agent_executor = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
