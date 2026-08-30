from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from socialgen import generate_post # Import your existing AI function

load_dotenv()
app = FastAPI()

# 1. Setup CORS so React can talk to Python - localhost for dev, plus
# whatever the deployed frontend's origin is (set as ALLOWED_ORIGINS on
# the host, e.g. the Netlify URL) so the hosted app isn't blocked.
DEFAULT_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
extra_origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "").split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=DEFAULT_ORIGINS + extra_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Health check route - visiting the deployed URL directly otherwise
# hits FastAPI's default 404 ({"detail":"Not Found"}), same pattern as
# the Notes App backend's root route.
@app.get("/")
async def root():
    return {"message": "AI Content Generator API is running!"}

# 3. Define the data shape the Frontend sends
class PostRequest(BaseModel):
    topic: str
    platform: str

# 4. The API Endpoint
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
