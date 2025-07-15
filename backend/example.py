"""Practical example of WeviateService and OpenAI usage."""

import os
from dotenv import load_dotenv
from backend.src.weviate_service import create_weviate_service
from backend.src.openai_service import create_openai_service

# Load environment variables
load_dotenv()


def main():
    """WeviateService and OpenAI usage example."""
    
    print("=== Backend Services Example ===")
    
    # Test OpenAI Service
    print("\n🤖 Testing OpenAI Service...")
    openai_service = create_openai_service()
    if openai_service.connect():
        print("✅ Connected to OpenAI")
        response = openai_service.generate_text("Say hello in a friendly way!")
        print(f"AI Response: {response}")
    else:
        print("❌ Failed to connect to OpenAI")
    
    # Test Weaviate Service
    print("\n🔍 Testing Weaviate Service...")
    service = create_weviate_service("YourCollectionName")
    
    if service.connect():
        print("✅ Connected to Weaviate")
        
        # Add a document
        document = {
            "id": "doc_001",
            "title": "Bug Report",
            "description": "Authentication system fails with error 500",
            "category": "backend",
            "priority": "high"
        }
        
        if service.add_document(document):
            print("✅ Document added successfully")
        
        # Add multiple documents
        documents = [
            {
                "id": "doc_002",
                "title": "Feature Request",
                "description": "Implement dark mode in interface",
                "category": "frontend",
                "priority": "medium"
            },
            {
                "id": "doc_003", 
                "title": "Performance Issue",
                "description": "Dashboard loads very slowly",
                "category": "performance",
                "priority": "high"
            }
        ]
        
        if service.add_documents_batch(documents):
            print("✅ Batch documents added")
        
        # Search documents
        results = service.query("performance issues", limit=5)
        print(f"\n📋 Search results ({len(results)}):")
        for ticket in results:
            print(f"- {ticket['id']}: {ticket['description']}")
        
        # Additional search example
        tech_results = service.query("technical issues", limit=3)
        print(f"\n🔍 Technical results ({len(tech_results)}):")
        for ticket in tech_results:
            print(f"- {ticket['id']}: {ticket['description']}")
        
        service.disconnect()
        print("\n✅ Disconnected from Weaviate")
        
    else:
        print("❌ Failed to connect to Weaviate")


if __name__ == "__main__":
    main() 