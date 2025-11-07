from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set OpenAI API key
API_KEY = os.getenv("AIzaSyCDx6vuO0_yzXI3trvw3h-kwHLvZcyt73E")

class ChatMessage(BaseModel):
    message: str

def get_ai_response(user_message: str) -> str:
    """Get response from OpenAI API"""
    try:
        # Using the updated OpenAI v1.x API
        client = openai.OpenAI(API_KEY=API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful cyber AI assistant. Be concise and helpful."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return f"I apologize, but I encountered an error: {str(e)}"

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    with open("app/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Cyber AI Assistant Backend is running!",
        "version": "1.0"
    }

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    """Handle chat messages"""
    try:
        if not chat_message.message or not chat_message.message.strip():
            return JSONResponse(
                {"error": "Message cannot be empty"},
                status_code=400
            )
        
        user_message = chat_message.message.strip()
        ai_reply = get_ai_response(user_message)
        
        return {
            "reply": ai_reply,
            "status": "success"
        }
    
    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")
        return JSONResponse(
            {"error": f"Server error: {str(e)}"},
            status_code=500
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    api_key_set = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "status": "healthy",
        "openai_key_configured": api_key_set
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)