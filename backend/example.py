"""Practical example of WeviateService usage."""

from backend.src.weviate_service import create_weviate_service


def main():
    """WeviateService usage example."""
    
    # Create service for your collection
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
        
        # Search with filter
        filter_criteria = {"path": ["category"], "operator": "Equal", "valueText": "backend"}
        filtered_results = service.query_with_filter("system error", filter_criteria, limit=3)
        print(f"\n🔍 Filtered results ({len(filtered_results)}):")
        for ticket in filtered_results:
            print(f"- {ticket['id']}: {ticket['description']}")
        
        service.disconnect()
        print("\n✅ Disconnected from Weaviate")
        
    else:
        print("❌ Failed to connect to Weaviate")


if __name__ == "__main__":
    main() 