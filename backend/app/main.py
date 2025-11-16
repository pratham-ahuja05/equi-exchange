from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router




# 🔥 LOAD .env here (CRITICAL FIX)
import os
from dotenv import load_dotenv

# This loads environment variables from /backend/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Debug print to verify the key loads
print("GEMINI KEY LOADED:", os.getenv("GEMINI_API_KEY") is not None)

app = FastAPI(title="EquiExchange Backend")

@app.get("/")
def root():
    return {
        "message": "EquiExchange API is running",
        "market_service_enabled": os.getenv("ALPHA_VANTAGE_API_KEY") is not None,
        "features": {
            "ai_negotiation": True,
            "market_integration": True,
            "blockchain_recording": True
        }
    }

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # Allow all for development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(router)
