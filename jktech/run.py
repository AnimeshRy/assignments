#!/usr/bin/env python3
"""
Script to run the document RAG application.
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment variables or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "True").lower() == "true"

    print(f"Starting server at http://{host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)
