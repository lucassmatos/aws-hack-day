"""Backend main application."""

import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from .config import get_settings
from .openai_service import create_ticket_agent
from .dynamodb_client import save_ticket, get_ticket_by_id, list_tickets, query_tickets_by_category
from .weviate_service import create_weviate_service
from .ticket_types import Ticket
from typing import List

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
async def create_ticket(request: dict):
    """Create a new ticket with AI-generated solution and save to both databases."""
    try:
        # Extract problem from request
        problem = request.get("problem")
        if not problem:
            raise HTTPException(status_code=400, detail="Problem description is required")
        
        # Call ticket agent to generate solution
        ticket_agent = create_ticket_agent()
        ticket = await ticket_agent.create_ticket_with_solution(problem)
        
        # Save to DynamoDB first (already done in create_ticket_with_solution)
        print(f"✅ Ticket {ticket['id']} saved to DynamoDB")
        
        # Save to Weaviate
        weaviate_service = create_weviate_service("Tickets")
        if weaviate_service.connect():
            # Prepare ticket for Weaviate (using compatible field names)
            weaviate_doc = {
                "issue_id": ticket["id"],
                "problem": ticket["problem"],
                "solution": ticket["solution"],
                "category": ticket["category"],
                "created_at": ticket["created_at"]
            }
            
            if weaviate_service.add_document(weaviate_doc):
                print(f"✅ Ticket {ticket['id']} saved to Weaviate")
            else:
                print(f"⚠️ Failed to save ticket {ticket['id']} to Weaviate")
            
            weaviate_service.disconnect()
        else:
            print("⚠️ Could not connect to Weaviate")
        
        return ticket
        
    except Exception as e:
        print(f"Error creating ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating ticket: {str(e)}")


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