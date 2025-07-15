# Backend Service

Backend service with Weaviate integration.

## Configuration

1. Install dependencies:
```bash
cd backend
pip install -e .
```

2. Configure the `.env` file:
```bash
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your-weaviate-api-key
```

## WeviateService Usage

```python
from backend.src.weviate_service import create_weviate_service

# Create service
service = create_weviate_service("YourCollectionName")

# Connect
if service.connect():
    # Add document
    doc = {"id": "1", "description": "Example document"}
    service.add_document(doc)
    
    # Search documents
    results = service.query("semantic search", limit=5)
    
    # Disconnect
    service.disconnect()
```

## Structure

- `src/weaviate_client.py` - Weaviate Client
- `src/weviate_service.py` - Main interface
- `src/types.py` - Type definitions
- `src/main.py` - FastAPI API 