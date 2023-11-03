import uvicorn
from fastapi import FastAPI

import openai
openai.api_base = "https://api.chatanywhere.com.cn/v1"

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

from common.utils import Utils
from common.agent_utils import base_suffix, custom_suffix_filter, custom_suffix_sim
from common.agent_utils import create_retriever_filter, create_retriever_sim

import requests

#prepare db, llm and db tools
db = SQLDatabase.from_uri('postgresql+psycopg2://flowise:flowise@localhost/metastore')
llm = ChatOpenAI(model='gpt-4-0613', temperature=0, openai_api_key = Utils.get_openai_key())
toolkit = SQLDatabaseToolkit(db=db, llm=llm)


#create agent
agent_1 = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    suffix=base_suffix
)

custom_tool_list_1 = [ create_retriever_sim(openai_key=Utils.get_openai_key())]
agent_sim_2 = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    extra_tools=custom_tool_list_1,
    suffix=custom_suffix_sim + base_suffix,
)

custom_tool_list_2 = [create_retriever_filter(opai_key=Utils.get_openai_key())]
agent_filter_3 = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    extra_tools=custom_tool_list_2,
    suffix=custom_suffix_filter + base_suffix,
)

agent_compose = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    extra_tools=custom_tool_list_1 + custom_tool_list_2,
    suffix=custom_suffix_sim + custom_suffix_filter + base_suffix,
)

def run_agent(question):
    response = agent_1.run(question)
    return response


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ask/{question}")
async def ask_quest(question: str):
    print("incoming qestion: " + question)
    response = agent_1.run(question)
    return {"message": response}


from pydantic import BaseModel

class Item(BaseModel):
    content: str

@app.post("/database_query/")
async def database_query(item: Item):
    # Extract the content from the request body
    question = item.content
    print(f"Received content: {question}")
    response = agent_1.run(question)
    #response = run_agent(str(question))
    return response

@app.post("/database_query_sim/")
async def database_query(item: Item):
    # Extract the content from the request body
    question = item.content
    print(f"Received content: {question}")
    response = agent_sim_2.run(question)
    #response = run_agent(str(question))
    return response

@app.post("/database_query_filter/")
async def database_query(item: Item):
    # Extract the content from the request body
    question = item.content
    print(f"Received content: {question}")
    response = agent_filter_3.run(question)
    #response = run_agent(str(question))
    return response

@app.post("/database_query_compose/")
async def database_query(item: Item):
    # Extract the content from the request body
    question = item.content
    print(f"Received content: {question}")
    response = agent_compose.run(question)
    #response = run_agent(str(question))
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)
