from fastapi import Request, FastAPI
import uvicorn
from pydantic import BaseModel

from apps.autogen.controller import api_controller

app = FastAPI()
app.include_router(api_controller.router)


class xxx(BaseModel):
    sessionId: str
@app.post("/xxx")
async def prepareAgents(request: Request):
    return await request.body()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3300)
