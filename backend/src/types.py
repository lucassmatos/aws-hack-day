"""Types definitions for the backend."""

from typing import TypedDict


class Ticket(TypedDict):
    """Ticket type definition."""
    id: str
    problem: str
    solution: str