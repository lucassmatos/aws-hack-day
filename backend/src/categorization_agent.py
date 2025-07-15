"""Categorization agent for ticket classification."""

from typing import Dict, Any, Optional
from .openai_service import OpenAIService


class CategorizationAgent:
    """Agent for categorizing customer support tickets."""
    
    def __init__(self):
        """Initialize the categorization agent."""
        self.openai_service = OpenAIService()
        self.categories = {
            "booking": "Booking & Reservation Issues",
            "payment": "Payment & Billing Issues", 
            "property": "Property & Stay Issues",
            "host": "Host/Seller Issues",
            "technical": "Technical & App Issues"
        }
        
    def categorize_ticket(self, problem: str) -> Dict[str, Any]:
        """Categorize a ticket based on its problem description."""
        if not self.openai_service.connect():
            return {
                "category": "technical",
                "confidence": 0.5,
                "reasoning": "Unable to connect to AI service"
            }
        
        prompt = f"""
        You are a customer support ticket categorization system for Acme Rentals, a cabin rental marketplace.
        
        Analyze the following customer problem and categorize it into one of these categories:
        
        1. booking - Booking & Reservation Issues (reservations, availability, modifications, cancellations)
        2. payment - Payment & Billing Issues (charges, refunds, payment methods, billing disputes)
        3. property - Property & Stay Issues (property conditions, amenities, check-in/out, cleanliness)
        4. host - Host/Seller Issues (host communication, host behavior, property listing accuracy)
        5. technical - Technical & App Issues (app bugs, website problems, login issues, platform functionality)
        
        Customer Problem: "{problem}"
        
        Respond with JSON format:
        {{
            "category": "category_key",
            "confidence": 0.95,
            "reasoning": "Brief explanation of why this category was chosen"
        }}
        
        Only respond with valid JSON, no additional text.
        """
        
        try:
            response = self.openai_service.generate_text(prompt, max_tokens=200)
            
            # Parse JSON response
            import json
            result = json.loads(response)
            
            # Validate category exists
            if result.get("category") not in self.categories:
                return {
                    "category": "technical",
                    "confidence": 0.5,
                    "reasoning": "Invalid category returned by AI"
                }
            
            return result
            
        except Exception as e:
            print(f"Error categorizing ticket: {e}")
            return {
                "category": "technical",
                "confidence": 0.5,
                "reasoning": "Error during categorization"
            }
    
    def get_category_name(self, category_key: str) -> str:
        """Get the full category name from the key."""
        return self.categories.get(category_key, "Unknown Category")