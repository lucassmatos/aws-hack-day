"""Backend main application."""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .config import get_settings

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
from types import Ticket
from typing import List

app = FastAPI()


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
def create_ticket(ticket: dict):  # Accepts problem and solution, assigns id
    ticket_id = str(uuid4())
    new_ticket = {
        "id": ticket_id,
        "problem": ticket.get("problem"),
        "solution": ticket.get("solution")
    }
    tickets_db[ticket_id] = new_ticket
    return new_ticket

@app.get("/tickets/", response_model=List[Ticket])
def get_tickets():
    return list(tickets_db.values())

@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: str):
    ticket = tickets_db.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        reload=settings.debug
    ) 