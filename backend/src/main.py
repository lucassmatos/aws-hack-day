"""Backend main application."""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from backend.src.config import get_settings

# Load environment variables from .env file
load_dotenv()

# Get settings
settings = get_settings()

app = FastAPI(
    title="AWS Hack Day Backend",
    description="Backend service with Weaviate and OpenAI integration",
    version="0.1.0",
    debug=settings.debug
)


@app.get("/")
def root():
    return {
        "message": "Backend API",
        "debug": settings.debug,
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config")
def config_status():
    """Check configuration status."""
    return {
        "weaviate_configured": bool(settings.weaviate_url and settings.weaviate_api_key),
        "openai_configured": bool(settings.openai_api_key),
        "aws_configured": bool(settings.aws_access_key_id and settings.aws_secret_access_key),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        reload=settings.debug
    ) 