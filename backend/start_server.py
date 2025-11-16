#!/usr/bin/env python3
"""
Simple script to start the backend server
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("Starting EquiExchange Backend Server...")
    print(f"GEMINI_API_KEY loaded: {os.getenv('GEMINI_API_KEY') is not None}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )