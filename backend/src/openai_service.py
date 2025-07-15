"""OpenAI service for AI operations."""

from typing import Optional, Dict, Any
from openai import OpenAI
from config import get_openai_config


class OpenAIService:
    """Service for handling OpenAI operations."""
    
    def __init__(self):
        """Initialize OpenAI service."""
        self.client: Optional[OpenAI] = None
        self.config = get_openai_config()
    
    def connect(self) -> bool:
        """Connect to OpenAI."""
        if not self.config:
            print("OpenAI API key not configured")
            return False
        
        try:
            self.client = OpenAI(api_key=self.config["api_key"])
            return True
        except Exception as e:
            print(f"Error connecting to OpenAI: {e}")
            return False
    
    def generate_text(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Generate text using OpenAI."""
        if not self.client:
            return "OpenAI client not connected"
        
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens or self.config["max_tokens"]
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""
    
    def generate_embedding(self, text: str) -> list:
        """Generate embedding for text."""
        if not self.client:
            return []
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []


def create_openai_service() -> OpenAIService:
    """Create OpenAI service instance."""
    return OpenAIService()


# Public API
openai_api = {
    "OpenAIService": OpenAIService,
    "create_openai_service": create_openai_service,
} 