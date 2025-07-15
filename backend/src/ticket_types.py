"""Types definitions for the backend."""

from typing import TypedDict, Optional


class Ticket(TypedDict):
    """Ticket type definition."""
    id: str
    problem: str
    solution: Optional[str]
    category: str
    created_at: Optional[str]  # ISO timestamp
    updated_at: Optional[str]  # ISO timestamp