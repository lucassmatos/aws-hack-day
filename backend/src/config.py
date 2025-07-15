"""Configuration management for backend service."""

import os
from typing import Dict, Any, Optional
from functools import lru_cache


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        """Initialize settings from environment variables."""
        # Server Configuration
        self.debug: bool = os.getenv("DEBUG", "False").lower() == "true"
        self.port: int = int(os.getenv("PORT", "8000"))
        self.host: str = os.getenv("HOST", "0.0.0.0")
        
        # Weaviate Configuration
        self.weaviate_url: str = os.getenv("WEAVIATE_URL", "")
        self.weaviate_api_key: str = os.getenv("WEAVIATE_API_KEY", "")
        
        # OpenAI Configuration
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
        self.openai_max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        
        # AWS Configuration
        self.aws_region: str = os.getenv("AWS_REGION", "us-east-1")
        self.aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
        self.aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
        
        # Database
        self.database_url: str = os.getenv("DATABASE_URL", "")
        
        # Security
        self.api_secret_key: str = os.getenv("API_SECRET_KEY", "")


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


def get_weaviate_config() -> Dict[str, str]:
    """Get Weaviate configuration from settings."""
    settings = get_settings()
    
    if not settings.weaviate_url or not settings.weaviate_api_key:
        return {}
    
    return {
        "url": settings.weaviate_url,
        "api_key": settings.weaviate_api_key,
    }


def get_openai_config() -> Dict[str, Any]:
    """Get OpenAI configuration from settings."""
    settings = get_settings()
    
    if not settings.openai_api_key:
        return {}
    
    return {
        "api_key": settings.openai_api_key,
        "model": settings.openai_model,
        "max_tokens": settings.openai_max_tokens,
    }


def get_aws_config() -> Dict[str, str]:
    """Get AWS configuration from settings."""
    settings = get_settings()
    
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        return {}
    
    return {
        "aws_access_key_id": settings.aws_access_key_id,
        "aws_secret_access_key": settings.aws_secret_access_key,
        "region_name": settings.aws_region,
    }


# Public API
config_api = {
    "get_settings": get_settings,
    "get_weaviate_config": get_weaviate_config,
    "get_openai_config": get_openai_config,
    "get_aws_config": get_aws_config,
} 