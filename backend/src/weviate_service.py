"""Weviate service for document management."""

from typing import List, Optional, Dict, Any
import weaviate
from weaviate.classes.query import Filter
from types import Ticket
from weaviate_client import create_weaviate_client, close_client


class WeviateService:
    """Service for handling Weviate operations."""
    
    def __init__(self, collection_name: str = "Documents"):
        """Initialize WeviateService."""
        self.client: Optional[weaviate.WeaviateClient] = None
        self.collection_name = collection_name
    
    def connect(self) -> bool:
        """Connect to Weaviate."""
        self.client = create_weaviate_client()
        return self.client is not None
    
    def disconnect(self) -> None:
        """Disconnect from Weaviate."""
        if self.client:
            close_client(self.client)
            self.client = None
    
    def add_document(self, document: Dict[str, Any]) -> bool:
        """Add a document to Weaviate collection."""
        if not self.client:
            print("Client not connected")
            return False
        
        try:
            collection = self.client.collections.get(self.collection_name)
            collection.data.insert(properties=document)
            return True
            
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    def add_documents_batch(self, documents: List[Dict[str, Any]]) -> bool:
        """Add multiple documents to Weaviate collection in batch."""
        if not self.client:
            print("Client not connected")
            return False
        
        try:
            collection = self.client.collections.get(self.collection_name)
            
            with collection.batch.fixed_size(batch_size=100) as batch:
                for doc in documents:
                    batch.add_object(properties=doc)
                    
                    if batch.number_errors > 10:
                        print("Batch import stopped due to too many errors")
                        return False
            
            failed_objects = collection.batch.failed_objects
            if failed_objects:
                print(f"Number of failed documents: {len(failed_objects)}")
                return False
                
            return True
            
        except Exception as e:
            print(f"Error adding documents in batch: {e}")
            return False
    
    def query(self, search_query: str, limit: int = 10) -> List[Ticket]:
        """Query documents from Weaviate using semantic search."""
        if not self.client:
            print("Client not connected")
            return []
        
        try:
            collection = self.client.collections.get(self.collection_name)
            response = collection.query.near_text(
                query=search_query,
                limit=limit
            )
            
            tickets: List[Ticket] = []
            for obj in response.objects:
                # Extract properties and convert to strings
                doc_id = obj.properties.get("id", str(obj.uuid))
                doc_description = obj.properties.get("description", "")
                
                tickets.append({
                    "id": str(doc_id),
                    "description": str(doc_description)
                })
            
            return tickets
            
        except Exception as e:
            print(f"Error querying Weaviate: {e}")
            return []
    



def create_weviate_service(collection_name: str = "Documents") -> WeviateService:
    """Create WeviateService instance."""
    return WeviateService(collection_name)


# Public API
weviate_api = {
    "WeviateService": WeviateService,
    "create_weviate_service": create_weviate_service,
} 