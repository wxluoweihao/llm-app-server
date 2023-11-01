import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_statements")
async def get_sql_meta(question: str):
    return """
    
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
