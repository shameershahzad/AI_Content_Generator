from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from socialgen import generate_post # Import your existing AI function

load_dotenv()
app = FastAPI()

# 1. Setup CORS so React (port 5173) can talk to Python (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define the data shape the Frontend sends
class PostRequest(BaseModel):
    topic: str
    platform: str

# 3. The API Endpoint
@app.post("/generate")
async def handle_request(data: PostRequest):
    try:
        # Calls your LangChain/Gemini function
        content = generate_post(
            topic=data.topic, 
            platform=data.platform, 
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        return {"content": content}
    except Exception as e:
        return {"content": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)