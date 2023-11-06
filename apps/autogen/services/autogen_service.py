from typing import Optional, List, Dict, Union, Callable

import autogen
import requests
from autogen import Agent, ConversableAgent, config_list_from_json
from pydantic import BaseModel

class AgentConfig(BaseModel):
    name: str
    url: str
class RemoteAgent(ConversableAgent):

    def __init__(
            self,
            sessionId: str,
            name: str,
            connectUrl: str,
            isAdmin: bool,
            system_message="""
            You are a agent that must response other agent with a answer. 
            When you find an answer, verify the answer carefully. If answer does not look like a answer, then find a new answer. 
            After you verify the answer and the answer is correct, include verifiable evidence in your response if possible.
            Reply "TERMINATE" in the end when everything is done.
            """,
            llm_config=None,
            is_termination_msg=None,
            max_consecutive_auto_reply=False,
            human_input_mode="NEVER",
            code_execution_config=False,
            **kwargs,
    ):
        self.sessionId = sessionId
        self.isAdmin = isAdmin
        self.agentName = name
        self.connectUrl = connectUrl
        super().__init__(
            name,
            system_message,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            code_execution_config=code_execution_config,
            llm_config=llm_config,
            **kwargs,
        )



    def generate_reply(self, messages: Optional[List[Dict]] = None, sender: Optional[Agent] = None,
                       exclude: Optional[List[Callable]] = None) -> Union[str, Dict, None]:
        url = 'https://www.w3schools.com/python/demopage.php'
        response = requests.post(url, json={
            'question': messages[-1]
        })

        print('response from agent: ' + self.name + ', content: ' + response)
        return response.txt

    async def a_generate_reply(self, messages: Optional[List[Dict]] = None, sender: Optional[Agent] = None,
                               exclude: Optional[List[Callable]] = None) -> Union[str, Dict, None]:
        return await super().a_generate_reply(messages, sender, exclude)


class AutoGenSession:
    def __init__(self, sessionId: str, agentsList: List[AgentConfig]):
        self.sessionId = sessionId

        config_list = [
            {
                'model': 'gpt-4',
                'api_key': 'sk-Svpb5RMtoyknkzZOa43EYd0UnBWFaUMqxP7AOCQJ2cQ08vvl',
            }
        ]

        # initialize worker agents for the session
        self.agents = []

        for agentConfig in agentsList:
            agentName = agentConfig.name
            agentConnectUrl = agentConfig.url
            self.agents.append(RemoteAgent(sessionId, agentName, agentConnectUrl, False))

        # initialize master agent for the session
        self.master_agent = ConversableAgent(
            name="admin-agent-" + self.sessionId,
            system_message="""
            You are a admin agent, which responsible for asking question to other agents to answer input questions
            When you find an answer, verify the answer carefully. If answer does not look like a answer, then find a new answer.
            After you verify the answer and the answer is correct, include verifiable evidence in your response if possible.
            Reply answer in the end when everything is done.
            """,
            llm_config = {"config_list": config_list},
            code_execution_config = False,
            human_input_mode="TERMINATE",
            default_auto_reply="Sorry, I can't find the answer. Please provide more information."
        )
        # self.agents.append(self.master_agent)

        # create groupchat
        self.groupchat = autogen.GroupChat(agents=self.agents, messages=[], max_round=12)
        self.manager = autogen.GroupChatManager(groupchat=self.groupchat, llm_config={"config_list": config_list})


class AutoGenService:
    def __init__(self):
        self.sessionMap = {}

    def createOrGetSession(self, sessionId, agentsList):
        if sessionId in self.sessionMap:
            print("session '" + sessionId + "' already exists. ")
        else:
            # create new session for autogen service
            print("session '" + sessionId + "' not exists. creating a new session")
            autoGenSession = AutoGenSession(sessionId, agentsList)
            self.sessionMap.update({sessionId : autoGenSession})
            print("session created.")
    
    def processInput(self, sessionId, msg:str):
        autoGenSession:AutoGenSession = self.sessionMap.get(sessionId)
        autoGenSession.manager.run_chat(
            messages={"content": msg, "role": "user"},
            sender=autoGenSession.manager,
        )
