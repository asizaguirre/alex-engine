from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests
import os


app = FastAPI(
    title="AlEx Local AI Engine",
    version="2.0"
)


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

API_KEY = os.getenv(
    "ALEX_ENGINE_API_KEY",
    "7221971d3bb6ec4118585a821e92378c446fd4267297a62c89e56906a4399287"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():

    return {
        "status": "UP",
        "engine": "AlEx",
        "ollama": "connected"
    }



@app.post("/api/agents/chat")
def agent_chat(
    request: ChatRequest,
    x_api_key: str = Header(None)
):

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )


    payload = {

        "model": "qwen2.5-coder:7b",

        "prompt": request.message,

        "stream": False

    }


    response = requests.post(

        f"{OLLAMA_URL}/api/generate",

        json=payload,

        timeout=120

    )


    result = response.json()


    return {

        "engine": "AlEx",

        "response": result.get("response",""),

        "model": "qwen2.5-coder:7b"

    }



@app.get("/chat")
def old_chat(message:str):

    payload = {

        "model":"qwen2.5-coder:7b",

        "prompt":message,

        "stream":False

    }


    response=requests.post(

        f"{OLLAMA_URL}/api/generate",

        json=payload

    )


    return response.json()
