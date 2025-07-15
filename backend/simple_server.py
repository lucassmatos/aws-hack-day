"""Simple standalone server for testing."""

import os
import sys
import json
from uuid import uuid4
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from fastapi import FastAPI, HTTPException
    from typing import List, Dict, Any
    
    # Load environment variables
    load_dotenv()
    
    app = FastAPI(
        title="AWS Hack Day Backend",
        description="Backend service with AI agents",
        version="0.1.0"
    )
    
    # Mock ticket storage
    tickets_db = {}
    
    # Mock categories
    categories = {
        "booking": "Booking & Reservation Issues",
        "payment": "Payment & Billing Issues", 
        "property": "Property & Stay Issues",
        "host": "Host/Seller Issues",
        "technical": "Technical & App Issues"
    }
    
    @app.get("/")
    def root():
        return {"message": "Backend API is running", "version": "0.1.0"}
    
    @app.get("/health")
    def health():
        return {"status": "ok"}
    
    @app.get("/config")
    def config_status():
        return {
            "weaviate_configured": bool(os.getenv("WEAVIATE_URL") and os.getenv("WEAVIATE_API_KEY")),
            "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
            "categories": categories
        }
    
    @app.post("/tickets/")
    def create_ticket(ticket: Dict[str, Any]):
        """Create a new ticket with mock AI processing."""
        ticket_id = str(uuid4())
        problem = ticket.get("problem", "")
        
        # Mock categorization (simple keyword matching)
        category = "technical"  # default
        problem_lower = problem.lower()
        if any(word in problem_lower for word in ["booking", "reservation", "cancel", "modify"]):
            category = "booking"
        elif any(word in problem_lower for word in ["payment", "billing", "charge", "refund"]):
            category = "payment"
        elif any(word in problem_lower for word in ["property", "room", "clean", "amenity"]):
            category = "property"
        elif any(word in problem_lower for word in ["host", "owner", "communication"]):
            category = "host"
        
        # Mock solution
        solution = f"Thank you for contacting us about your {categories[category].lower()}. We will review your request and get back to you within 24 hours."
        
        new_ticket = {
            "id": ticket_id,
            "problem": problem,
            "solution": solution,
            "category": category,
            "priority": "medium",
            "status": "open"
        }
        
        tickets_db[ticket_id] = new_ticket
        return new_ticket
    
    @app.get("/tickets/")
    def get_tickets():
        return list(tickets_db.values())
    
    @app.get("/tickets/{ticket_id}")
    def get_ticket(ticket_id: str):
        ticket = tickets_db.get(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket
    
    @app.post("/categorize")
    def categorize_problem(request: Dict[str, Any]):
        """Mock categorization endpoint."""
        problem = request.get("problem", "")
        if not problem:
            raise HTTPException(status_code=400, detail="Problem description is required")
        
        # Mock categorization logic
        category = "technical"
        problem_lower = problem.lower()
        if any(word in problem_lower for word in ["booking", "reservation", "cancel", "modify"]):
            category = "booking"
        elif any(word in problem_lower for word in ["payment", "billing", "charge", "refund"]):
            category = "payment"
        elif any(word in problem_lower for word in ["property", "room", "clean", "amenity"]):
            category = "property"
        elif any(word in problem_lower for word in ["host", "owner", "communication"]):
            category = "host"
        
        return {
            "problem": problem,
            "category": category,
            "category_name": categories[category],
            "confidence": 0.85,
            "reasoning": f"Categorized as {category} based on keywords"
        }
    
    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Please install required dependencies:")
    print("pip install fastapi uvicorn python-dotenv")
    sys.exit(1)