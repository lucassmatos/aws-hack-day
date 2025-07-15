"""Backend main application."""

import os
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from .config import get_settings
from .types import Ticket
from .categorization_agent import CategorizationAgent
from .solution_agent import SolutionAgent
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

# In-memory storage for tickets
tickets_db = {}

# Initialize AI agents
categorization_agent = CategorizationAgent()
solution_agent = SolutionAgent()


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
def create_ticket(ticket: dict):  # Accepts problem, uses AI for categorization and solution
    ticket_id = str(uuid4())
    problem = ticket.get("problem", "")
    
    # Use categorization agent to classify the ticket
    categorization_result = categorization_agent.categorize_ticket(problem)
    category = categorization_result.get("category", "technical")
    
    # Use solution agent to suggest a solution
    solution_result = solution_agent.suggest_solution(problem, category)
    solution = solution_result.get("solution", "Please contact our support team for assistance.")
    
    # Create ticket with AI-generated data
    new_ticket = {
        "id": ticket_id,
        "problem": problem,
        "solution": solution,
        "category": category,
        "priority": "medium",  # Default priority
        "status": "open"       # Default status
    }
    
    # Store ticket in database
    tickets_db[ticket_id] = new_ticket
    
    # Store ticket solution in Weaviate for future reference
    solution_agent.store_ticket_solution(new_ticket)
    
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

@app.post("/categorize")
def categorize_problem(request: dict):
    """Categorize a problem without creating a ticket."""
    problem = request.get("problem", "")
    if not problem:
        raise HTTPException(status_code=400, detail="Problem description is required")
    
    result = categorization_agent.categorize_ticket(problem)
    return {
        "problem": problem,
        "category": result.get("category"),
        "category_name": categorization_agent.get_category_name(result.get("category", "")),
        "confidence": result.get("confidence"),
        "reasoning": result.get("reasoning")
    }

@app.post("/suggest-solution")
def suggest_solution(request: dict):
    """Suggest a solution for a problem without creating a ticket."""
    problem = request.get("problem", "")
    category = request.get("category", "technical")
    
    if not problem:
        raise HTTPException(status_code=400, detail="Problem description is required")
    
    result = solution_agent.suggest_solution(problem, category)
    return {
        "problem": problem,
        "category": category,
        "solution": result.get("solution"),
        "confidence": result.get("confidence"),
        "similar_tickets": result.get("similar_tickets", [])
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        reload=settings.debug
    ) 