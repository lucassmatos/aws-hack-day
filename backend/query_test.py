#!/usr/bin/env python3
"""Simple query test script for the Tickets collection."""

import os
import sys
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.query import Filter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def query_tickets(search_query: str, limit: int = 5):
    """Query the Tickets collection with a search string."""
    print(f"=== Searching for: '{search_query}' ===")
    
    # Get environment variables
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_key = os.getenv("WEAVIATE_API_KEY")
    
    if not weaviate_url or not weaviate_key:
        print("❌ WEAVIATE_URL or WEAVIATE_API_KEY not configured")
        return False

    try:
        print("🔗 Connecting to Weaviate...")
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_key),
        )
        
        if not client.is_ready():
            print("❌ Weaviate is not ready")
            return False
            
        print("✅ Connected to Weaviate!")
        
        # Get the Tickets collection
        collection = client.collections.get("Tickets")
        
        # First try to get all tickets and filter manually since vectorizer isn't configured
        print(f"🔍 Searching for '{search_query}'...")
        
        # Get all tickets 
        response = collection.query.fetch_objects(limit=100)
        
        if not response.objects:
            print("📭 No tickets found in collection")
            return True
        
        # Filter results manually based on search query
        search_lower = search_query.lower()
        matching_results = []
        
        for obj in response.objects:
            problem = str(obj.properties.get("problem", "")).lower()
            solution = str(obj.properties.get("solution", "")).lower()
            category = str(obj.properties.get("category", "")).lower()
            
            # Check if search query appears in any field
            if (search_lower in problem or 
                search_lower in solution or 
                search_lower in category or
                any(word in problem or word in solution or word in category 
                    for word in search_lower.split())):
                matching_results.append(obj)
        
        # Limit results
        matching_results = matching_results[:limit]
        
        if not matching_results:
            print(f"📭 No results found for '{search_query}'")
            return True
            
        print(f"\n📋 Found {len(matching_results)} results:")
        print("-" * 80)
        
        for i, obj in enumerate(matching_results, 1):
            issue_id = str(obj.properties.get("issue_id", "Unknown"))
            category = str(obj.properties.get("category", "Unknown"))
            problem = str(obj.properties.get("problem", "No problem description"))
            solution = str(obj.properties.get("solution", "No solution"))
            
            print(f"\n{i}. ID: {issue_id}")
            print(f"   Category: {category}")
            print(f"   Problem: {problem[:150]}{'...' if len(problem) > 150 else ''}")
            print(f"   Solution: {solution[:150]}{'...' if len(solution) > 150 else ''}")
        
        print("\n" + "-" * 80)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return False
        
    finally:
        if 'client' in locals():
            client.close()
            print("✅ Connection closed")

def query_by_category(category: str):
    """Query tickets by specific category."""
    print(f"=== Searching by category: '{category}' ===")
    
    # Get environment variables
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_key = os.getenv("WEAVIATE_API_KEY")
    
    if not weaviate_url or not weaviate_key:
        print("❌ WEAVIATE_URL or WEAVIATE_API_KEY not configured")
        return False

    try:
        print("🔗 Connecting to Weaviate...")
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_key),
        )
        
        if not client.is_ready():
            print("❌ Weaviate is not ready")
            return False
            
        print("✅ Connected to Weaviate!")
        
        # Get the Tickets collection
        collection = client.collections.get("Tickets")
        
        # Use filter for exact category match
        response = collection.query.fetch_objects(
            filters=Filter.by_property("category").contains_any([category]),
            limit=10
        )
        
        if not response.objects:
            print(f"📭 No tickets found for category '{category}'")
            return True
            
        print(f"\n📋 Found {len(response.objects)} results:")
        print("-" * 80)
        
        for i, obj in enumerate(response.objects, 1):
            issue_id = str(obj.properties.get("issue_id", "Unknown"))
            category_val = str(obj.properties.get("category", "Unknown"))
            problem = str(obj.properties.get("problem", "No problem description"))
            
            print(f"\n{i}. ID: {issue_id}")
            print(f"   Category: {category_val}")
            print(f"   Problem: {problem[:200]}{'...' if len(problem) > 200 else ''}")
        
        print("\n" + "-" * 80)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during category search: {e}")
        return False
        
    finally:
        if 'client' in locals():
            client.close()
            print("✅ Connection closed")

def interactive_mode():
    """Run in interactive mode for multiple queries."""
    print("🎯 Interactive Query Mode")
    print("Commands:")
    print("  - Type a search query for text search")
    print("  - Type 'category:CategoryName' for category search")
    print("  - Type 'quit' to exit")
    print()
    
    while True:
        try:
            query = input("Search > ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
                
            if not query:
                print("Please enter a search query")
                continue
            
            if query.startswith("category:"):
                category = query[9:].strip()
                query_by_category(category)
            else:
                query_tickets(query)
            print()
            
        except KeyboardInterrupt:
            break
            
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        search_query = " ".join(sys.argv[1:])
        if search_query.startswith("category:"):
            category = search_query[9:].strip()
            query_by_category(category)
        else:
            query_tickets(search_query)
    else:
        # Interactive mode
        interactive_mode() 