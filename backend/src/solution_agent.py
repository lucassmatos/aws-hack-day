"""Solution suggestion agent for generating ticket solutions."""

from typing import Dict, Any, Optional, List
from .openai_service import OpenAIService
from .weviate_service import WeviateService


class SolutionAgent:
    """Agent for suggesting solutions to customer support tickets."""
    
    def __init__(self):
        """Initialize the solution suggestion agent."""
        self.openai_service = OpenAIService()
        self.weaviate_service = WeviateService()
        
    def suggest_solution(self, problem: str, category: str) -> Dict[str, Any]:
        """Suggest a solution based on the problem and category."""
        if not self.openai_service.connect():
            return {
                "solution": "Please contact our support team for assistance.",
                "confidence": 0.5,
                "similar_tickets": []
            }
        
        # Get similar tickets from Weaviate
        similar_tickets = self._find_similar_tickets(problem)
        
        # Generate solution using OpenAI
        solution = self._generate_solution(problem, category, similar_tickets)
        
        return {
            "solution": solution,
            "confidence": 0.8,
            "similar_tickets": similar_tickets
        }
    
    def _find_similar_tickets(self, problem: str) -> List[Dict[str, Any]]:
        """Find similar tickets using Weaviate semantic search."""
        if not self.weaviate_service.connect():
            return []
        
        try:
            # Query Weaviate for similar tickets
            results = self.weaviate_service.query_documents(
                query=problem,
                limit=3
            )
            
            return results if results else []
            
        except Exception as e:
            print(f"Error finding similar tickets: {e}")
            return []
    
    def _generate_solution(self, problem: str, category: str, similar_tickets: List[Dict[str, Any]]) -> str:
        """Generate a solution using OpenAI with context from similar tickets."""
        
        # Build context from similar tickets
        context = ""
        if similar_tickets:
            context = "\n\nSimilar past issues and solutions:\n"
            for i, ticket in enumerate(similar_tickets, 1):
                context += f"{i}. Problem: {ticket.get('problem', 'N/A')}\n"
                context += f"   Solution: {ticket.get('solution', 'N/A')}\n"
        
        # Category-specific guidance
        category_guidance = self._get_category_guidance(category)
        
        prompt = f"""
        You are a customer support agent for Acme Rentals, a cabin rental marketplace.
        
        Customer Problem: "{problem}"
        Category: {category}
        
        {category_guidance}
        {context}
        
        Provide a helpful, professional solution that:
        1. Addresses the specific problem
        2. Follows company policies
        3. Is actionable and clear
        4. Maintains a friendly, helpful tone
        
        Keep the solution concise (2-3 sentences maximum).
        """
        
        try:
            solution = self.openai_service.generate_text(prompt, max_tokens=300)
            return solution.strip() if solution else "Please contact our support team for assistance."
            
        except Exception as e:
            print(f"Error generating solution: {e}")
            return "Please contact our support team for assistance."
    
    def _get_category_guidance(self, category: str) -> str:
        """Get category-specific guidance for solution generation."""
        guidance = {
            "booking": """
            For booking issues:
            - Check availability and suggest alternative dates
            - Explain modification/cancellation policies
            - Provide booking confirmation details
            """,
            "payment": """
            For payment issues:
            - Verify payment method and billing information
            - Explain refund timelines (5-7 business days)
            - Direct to billing support for disputes
            """,
            "property": """
            For property issues:
            - Acknowledge the inconvenience
            - Offer immediate solutions when possible
            - Provide host contact information
            - Mention review process for property standards
            """,
            "host": """
            For host issues:
            - Mediate professionally between guest and host
            - Provide alternative communication methods
            - Escalate to host relations team if needed
            """,
            "technical": """
            For technical issues:
            - Provide basic troubleshooting steps
            - Suggest app updates or browser refresh
            - Escalate to technical support team
            """
        }
        
        return guidance.get(category, "Provide general customer support assistance.")
    
    def store_ticket_solution(self, ticket_data: Dict[str, Any]) -> bool:
        """Store ticket and solution in Weaviate for future reference."""
        if not self.weaviate_service.connect():
            return False
        
        try:
            # Store ticket data for future similarity searches
            self.weaviate_service.add_document(
                content=f"Problem: {ticket_data.get('problem', '')}\nSolution: {ticket_data.get('solution', '')}",
                metadata=ticket_data
            )
            return True
            
        except Exception as e:
            print(f"Error storing ticket solution: {e}")
            return False