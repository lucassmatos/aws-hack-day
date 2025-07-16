"""Weaviate client configuration."""

import os
import weaviate
from weaviate.classes.init import Auth
from typing import Optional
from config import get_weaviate_config


def create_weaviate_client() -> Optional[weaviate.WeaviateClient]:
    """Create and return Weaviate client."""
    config = get_weaviate_config()
    
    if not config:
        print("WEAVIATE_URL or WEAVIATE_API_KEY not configured")
        return None
    
    try:
        # Get OpenAI API key for headers if available
        openai_key = os.getenv("OPENAI_API_KEY")
        headers = {"X-Openai-Api-Key": openai_key} if openai_key else {}
        
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=config["url"],
            auth_credentials=Auth.api_key(config["api_key"]),
            headers=headers
        )
        
        if not client.is_ready():
            print("Weaviate client is not ready")
            return None
            
        return client
        
    except Exception as e:
        print(f"Error connecting to Weaviate: {e}")
        return None


def close_client(client: Optional[weaviate.WeaviateClient]) -> None:
    """Close Weaviate client connection."""
    if client:
        client.close()


# Public API
weaviate_client_api = {
    "create_weaviate_client": create_weaviate_client,
    "close_client": close_client,
} 