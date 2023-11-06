


from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from autogen import AssistantAgent, UserProxyAgent

app = FastAPI()

#Here setup the key for OpenAI API
config_list = [
    {
        'model': 'gpt-4',
        'api_key': 'sk-Svpb5RMtoyknkzZOa43EYd0UnBWFaUMqxP7AOCQJ2cQ08vvl',
    },
    
    ]





class Agent(BaseModel):
    name:str
    dsc:str
    type: str







@app.get("/data")
def send_response()-> str:
    message = "Yow it works"
    return message





#this is the API Post method 
@app.post("/createAgent")
def createAgent(agent:Agent) -> str:

    if agent.type == "user": 
        newAgent = createUserProxy(agent.name, agent.dsc)

        ## use this block to write more logic
    elif agent.type == "assistant":
        newAgent = createAssistantAgent(agent.name, agent.dsc)

        ## use this block to write more logic
    else:
        HTTPException(status_code=400, detail=f"Agent Type is wrong it can either be User or Assistant")

    return "Agent successfully created"
        
    





# this method creates Assistant agent instant for you and just provide name and description for agent
def createAssistantAgent(name:str, dsc:str) -> AssistantAgent:
    # Here 
    assistant = None
    if dsc is None:
        assistant = AssistantAgent(name, config_list)
    else: 
        assistant = AssistantAgent(name, dsc, config_list)


    return assistant

#this creates Human Agent 
def createUserProxy(name:str) -> UserProxyAgent:
    
    userAgent = UserProxyAgent(name, config_list)


    return userAgent







def call_Autogen(msg):
    print("it works, Right now I'm in the call_Autogen Method")
    from autogen import AssistantAgent, UserProxyAgent
    print(msg)
  

    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and OAI_CONFIG_LIST_sample.json
    # config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    # assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
    # user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
    # user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
    # This initiates an automated chat between the two agents to solve the task

    return "terminate"


