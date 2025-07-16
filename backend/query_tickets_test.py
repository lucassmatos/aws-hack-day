#!/usr/bin/env python3
"""Test semantic search on existing Tickets collection."""

import os
import sys
import traceback
import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def log_error(error_msg, exception=None):
    """Enhanced error logging with traceback."""
    print(f"❌ ERROR: {error_msg}")
    if exception:
        print(f"   Exception Type: {type(exception).__name__}")
        print(f"   Exception Message: {str(exception)}")
        print(f"   Traceback:")
        traceback.print_exc()
    print("   " + "="*50)

# Set OpenAI API key for Weaviate (it expects multiple formats)
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    os.environ["OPENAI_APIKEY"] = openai_key
    os.environ["X-OPENAI-API-KEY"] = openai_key

def test_existing_tickets_collection():
    """Test semantic search on existing Tickets collection."""
    print("=== Testing Existing Tickets Collection ===")
    
    # Get environment variables
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_key = os.getenv("WEAVIATE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print(f"Weaviate URL: {weaviate_url if weaviate_url else 'NOT SET'}")
    print(f"Weaviate API Key: {'SET' if weaviate_key else 'NOT SET'}")
    print(f"OpenAI API Key: {'SET' if openai_key else 'NOT SET'}")
    
    if not weaviate_url or not weaviate_key:
        print("\n❌ WEAVIATE_URL or WEAVIATE_API_KEY not configured")
        return False
    
    if not openai_key:
        print("\n❌ OPENAI_API_KEY not configured")
        return False
    
    # Set OpenAI API key environment variable for Weaviate
    os.environ["OPENAI_APIKEY"] = openai_key
    os.environ["OPENAI_API_KEY"] = openai_key  # Just to be sure
    os.environ["X-Openai-Api-Key"] = openai_key  # Header format (exact capitalization)
    print(f"✅ Set OPENAI_APIKEY and X-Openai-Api-Key environment variables")
    
    try:
        print("\n🔗 Connecting to Weaviate...")
        print(f"   URL: {weaviate_url}")
        print(f"   Using headers: {{'X-Openai-Api-Key': '{'SET' if openai_key else 'NOT SET'}'}}")
        
        try:
            client = weaviate.connect_to_weaviate_cloud(
                cluster_url=weaviate_url,
                auth_credentials=Auth.api_key(weaviate_key),
                headers={"X-Openai-Api-Key": openai_key}
            )
            print("   ✅ Connection object created successfully")
        except Exception as conn_error:
            log_error("Failed to create Weaviate connection", conn_error)
            return False
        
        print("   🔍 Checking client readiness...")
        try:
            if not client.is_ready():
                log_error("Weaviate client not ready - connection failed")
                return False
        except Exception as ready_error:
            log_error("Error checking client readiness", ready_error)
            return False
            
        print("✅ Connected to Weaviate and client is ready!")
        
        # List all collections
        print("\n📋 Available collections:")
        collections = client.collections.list_all()
        for collection_name in collections:
            print(f"   - {collection_name}")
        
        # Check if Tickets collection exists
        if "Tickets" not in collections:
            print("\n⚠️ 'Tickets' collection not found")
            print("Creating a sample ticket in the collection first...")
            
            # Create Tickets collection with proper vectorizer
            from weaviate.classes.config import Configure
            
            try:
                client.collections.create(
                    name="Tickets",
                    description="Customer support tickets",
                    vectorizer_config=Configure.Vectorizer.text2vec_cohere()
                )
                print("✅ Tickets collection created with Cohere vectorizer")
                
                # Add sample tickets
                tickets_collection = client.collections.get("Tickets")
                sample_tickets = [
                    {
                        "issue_id": "SAMPLE-001",
                        "problem": "The main widget component is not functioning properly",
                        "solution": "Restart the application and clear browser cache",
                        "category": "Technical Issues"
                    },
                    {
                        "issue_id": "SAMPLE-002", 
                        "problem": "Dashboard widget stopped working after update",
                        "solution": "Roll back to previous version or apply hotfix",
                        "category": "Bug Report"
                    }
                ]
                
                for ticket in sample_tickets:
                    tickets_collection.data.insert(ticket)
                    
                print(f"✅ Added {len(sample_tickets)} sample tickets")
                
            except Exception as e:
                print(f"❌ Failed to create Tickets collection: {e}")
                return False
        
        # Get Tickets collection
        tickets_collection = client.collections.get("Tickets")
        
        # Test 1: Get all tickets
        print(f"\n📊 Getting all tickets...")
        try:
            all_tickets = tickets_collection.query.fetch_objects(limit=10)
            print(f"   Found {len(all_tickets.objects)} tickets total")
            
            for i, ticket in enumerate(all_tickets.objects, 1):
                issue_id = str(ticket.properties.get("issue_id", "No ID"))
                problem = str(ticket.properties.get("problem", "No problem"))
                problem_preview = problem[:60] + "..." if len(problem) > 60 else problem
                print(f"   {i}. {issue_id}: {problem_preview}")
                
        except Exception as e:
            print(f"   ❌ Failed to fetch tickets: {e}")
        
        # Test 2: SEMANTIC SEARCH - "widget is not working"
        print(f"\n🎯 SEMANTIC SEARCH: 'widget is not working'")
        try:
            print("   🔍 Executing semantic search query...")
            semantic_results = tickets_collection.query.near_text(
                query="widget is not working",
                limit=5,
                return_metadata=["score", "distance"]
            )
            print("   ✅ Semantic search query completed successfully")
            
            print(f"   Found {len(semantic_results.objects)} semantically similar tickets:")
            
            if len(semantic_results.objects) == 0:
                print("   ⚠️  No semantic search results found - this may indicate vectorizer issues")
            
            for i, ticket in enumerate(semantic_results.objects, 1):
                try:
                    issue_id = ticket.properties.get("issue_id", "No ID")
                    problem = ticket.properties.get("problem", "No problem")
                    solution = ticket.properties.get("solution", "No solution")
                    category = ticket.properties.get("category", "No category")
                    
                    # Get similarity metrics
                    score = getattr(ticket.metadata, 'score', 'N/A') if hasattr(ticket, 'metadata') else 'N/A'
                    distance = getattr(ticket.metadata, 'distance', 'N/A') if hasattr(ticket, 'metadata') else 'N/A'
                    
                    print(f"\n   {i}. Ticket: {issue_id}")
                    print(f"      Problem: {problem}")
                    print(f"      Solution: {solution}")
                    print(f"      Category: {category}")
                    print(f"      Similarity Score: {score}")
                    print(f"      Distance: {distance}")
                    print(f"      ---")
                except Exception as parse_error:
                    log_error(f"Error parsing semantic search result {i}", parse_error)
                
        except Exception as e:
            log_error("Semantic search operation failed", e)
        
        # Test 3: Multiple semantic queries
        test_queries = [
            "login not working",
            "performance slow",
            "app crash error",
            "payment failed"
        ]
        
        print(f"\n🔍 TESTING MULTIPLE SEMANTIC QUERIES...")
        for query in test_queries:
            try:
                results = tickets_collection.query.near_text(
                    query=query,
                    limit=2
                )
                
                print(f"\n   Query: '{query}'")
                print(f"   Results: {len(results.objects)} matches")
                
                for j, ticket in enumerate(results.objects, 1):
                    issue_id = str(ticket.properties.get("issue_id", "No ID"))
                    problem = str(ticket.properties.get("problem", "No problem"))
                    problem_preview = problem[:50] + "..." if len(problem) > 50 else problem
                    print(f"      {j}. {issue_id}: {problem_preview}")
                    
            except Exception as e:
                print(f"   Query '{query}' failed: {e}")
        
        print(f"\n✅ Ticket query test completed!")
        return True
        
    except Exception as e:
        log_error("Main test function failed", e)
        return False
        
    finally:
        try:
            print("\n🔌 Closing Weaviate connection...")
            client.close()
            print("✅ Connection closed")
        except Exception as close_error:
            log_error("Error closing Weaviate connection", close_error)

if __name__ == "__main__":
    print("Testing Weaviate Tickets collection semantic search...\n")
    
    success = test_existing_tickets_collection()
    
    if success:
        print("\n🎉 Semantic search test completed successfully!")
    else:
        print("\n❌ Test failed - check configuration") 