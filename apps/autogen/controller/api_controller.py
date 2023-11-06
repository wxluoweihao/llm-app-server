import sys
import traceback
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from apps.autogen.services.autogen_service import AutoGenService, AgentConfig

auto_gen_service = AutoGenService()

router = APIRouter(
    prefix='/api/v1',
    tags=['api']
)

class InitMsg(BaseModel):
    sessionId: str
    agents: List[AgentConfig]

class SendMsg(BaseModel):
    sessionId: str
    message: str


@router.post("/prepOrInitAgents")
async def prepareAgents(initMsg: InitMsg):
    auto_gen_service.createOrGetSession(sessionId=initMsg.sessionId, agentsList=initMsg.agents)
    return {"message": "successfully init Autogen session."}
@router.post("/sendChatMsg")
async def prepareAgents(sendMsg: SendMsg):
    auto_gen_service.processInput(sessionId=sendMsg.sessionId, msg=sendMsg.message)
    return {"message": "successfully init Autogen session."}


