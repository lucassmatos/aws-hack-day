"""Weviate service for ticket management."""

from typing import List
from backend.src.types import Ticket


class WeviateService:
    """Service for handling Weviate operations."""
    
    def query(self) -> List[Ticket]:
        """Query tickets from Weviate."""
        # Mock data
        mock_tickets: List[Ticket] = [
            {"id": "1", "description": "Sistema de login não funciona"},
            {"id": "2", "description": "Erro 500 na API de pagamentos"},
            {"id": "3", "description": "Interface móvel com layout quebrado"},
            {"id": "4", "description": "Lentidão no carregamento da dashboard"},
            {"id": "5", "description": "Bug no formulário de cadastro"},
        ]
        return mock_tickets


def create_weviate_service() -> WeviateService:
    """Create WeviateService instance."""
    return WeviateService()


# Public API
weviate_api = {
    "WeviateService": WeviateService,
    "create_weviate_service": create_weviate_service,
} 