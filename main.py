from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI(title="Al-ex & Al-ia Platform")

# Templates
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    message: str
    agent: str = "al-ex"  # al-ex ou al-ia

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Al-ex & Al-ia</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #0f0f23; color: #00ffcc; }
            .chat { max-width: 800px; margin: 0 auto; }
            .message { margin: 15px 0; padding: 12px; border-radius: 8px; }
            .al-ex { background: #1a1a2e; border-left: 5px solid #00ffcc; }
            .al-ia { background: #16213e; border-left: 5px solid #ff00cc; }
            input { width: 100%; padding: 15px; font-size: 16px; background: #1e1e2f; border: none; color: white; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="chat">
            <h1>🤖 Al-ex & Al-ia</h1>
            <p>Converse com os dois agentes de IA</p>
            
            <div id="chat"></div>
            
            <input type="text" id="userInput" placeholder="Digite sua mensagem..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Enviar</button>
        </div>

        <script>
            async function sendMessage() {
                const input = document.getElementById("userInput");
                const message = input.value;
                if (!message) return;

                addMessage("Você", message, "user");

                const res = await fetch("/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: message})
                });
                const data = await res.json();
                
                addMessage("Al-ex", data.response || "Sem resposta", "al-ex");
                input.value = "";
            }

            function addMessage(sender, text, type) {
                const chat = document.getElementById("chat");
                chat.innerHTML += `<div class="message ${type}"><strong>${sender}:</strong> ${text}</div>`;
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.post("/chat")
async def chat(msg: Message):
    # Aqui você pode integrar RAG, Ollama, etc.
    return {"response": f"Olá! Sou o {msg.agent.upper()}. Recebi: {msg.message}. Como posso ajudar?"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)