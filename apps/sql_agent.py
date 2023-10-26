from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

from common.utils import Utils

db = SQLDatabase.from_uri("mysql+mysqlconnector://xxx:xxx@localhost:3306/sys")
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))


agent_executor = create_sql_agent(
    llm=OpenAI(openai_api_key = Utils.get_openai_key(), temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

agent_executor.run("list all tables in current database")