"""Types definitions for the backend."""

from typing import TypedDict, Optional


class Ticket(TypedDict):
    """Ticket type definition."""
    id: str
    problem: str
    solution: Optional[str]