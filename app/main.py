# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from .chain import get_response  # ✅ use our updated chain.py

app = FastAPI()

# Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    message = chat_message.message.strip()
    if not message:
        return JSONResponse({"reply": "Message cannot be empty"}, status_code=400)

    ai_reply = get_response(message)
    return {"reply": ai_reply, "status": "success"}

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    with open("app/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
