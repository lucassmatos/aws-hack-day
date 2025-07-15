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


@app.post("/tickets/", response_model=Ticket)
def create_ticket(ticket: dict):
    return save_ticket(ticket)


from fastapi import Query
from typing import Optional
import json

@app.get("/tickets/")
def get_tickets(
    limit: int = Query(50, description="Number of tickets per page"),
    page_token: Optional[str] = Query(None, description="DynamoDB pagination token as JSON string")
):
    token = None
    if page_token:
        token = json.loads(page_token)
    result = list_tickets(limit=limit, page_token=token)
    return result


@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: str):
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.get("/tickets/category/{category}", response_model=List[Ticket])
def get_tickets_by_category(category: str):
    return query_tickets_by_category(category)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        reload=settings.debug
    ) 