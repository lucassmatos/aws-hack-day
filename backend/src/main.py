"""Backend main application."""

from fastapi import FastAPI
from types import Ticket
from typing import List

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Backend API"}

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
    uvicorn.run(app, host="0.0.0.0", port=8000) 