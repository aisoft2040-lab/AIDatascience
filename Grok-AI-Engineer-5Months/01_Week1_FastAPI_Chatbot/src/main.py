import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Week1 FastAPI Chatbot Skeleton")


class EchoIn(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)


@app.get("/health")
def health():
    version = os.getenv("APP_VERSION", "dev")
    return {"status": "ok", "version": version}


@app.post("/echo")
def echo(payload: EchoIn):
    try:
        return {"message": payload.message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
