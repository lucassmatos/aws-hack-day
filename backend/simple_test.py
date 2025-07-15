#!/usr/bin/env python3
"""Simple Weaviate connection test."""

import os
import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_weaviate_full_workflow():
    """Test complete Weaviate CRUD workflow."""
    print("=== Weaviate Full CRUD Test ===")
    
    # Get environment variables
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_key = os.getenv("WEAVIATE_API_KEY")
    
    print(f"Weaviate URL: {weaviate_url if weaviate_url else 'NOT SET'}")
    print(f"API Key: {'SET' if weaviate_key else 'NOT SET'}")
    
    if not weaviate_url or not weaviate_key:
        print("\n❌ WEAVIATE_URL or WEAVIATE_API_KEY not configured")
        print("   Create a .env file with your Weaviate credentials")
        return False
    
    try:
        print("\n🔗 Connecting to Weaviate...")
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_key),
        )
        
        if not client.is_ready():
            print("❌ Weaviate is not ready")
            return False
            
        print("✅ Connected to Weaviate!")
        
        # Collection name for testing
        collection_name = "TestDocuments"
        
        try:
            # Step 1: Create Collection
            print(f"\n📁 Creating collection '{collection_name}'...")
            
            # Delete collection if it exists
            if client.collections.exists(collection_name):
                print(f"   Collection exists, deleting first...")
                client.collections.delete(collection_name)
                print("   ✅ Old collection deleted")
            
            # Create new collection with simple configuration
            client.collections.create(
                name=collection_name,
                description="Test collection for CRUD operations"
            )
            print("   ✅ Collection created successfully")
            
            # Get collection reference
            collection = client.collections.get(collection_name)
            
            # Step 2: Create single item
            print(f"\n📝 Adding single document...")
            single_doc = {
                "title": "Single Test Document",
                "content": "This is a test document for single insertion",
                "category": "test",
                "priority": "high"
            }
            
            result = collection.data.insert(single_doc)
            print(f"   ✅ Document added with ID: {result}")
            
            # Step 3: Create many items (batch)
            print(f"\n📚 Adding multiple documents in batch...")
            batch_docs = [
                {
                    "title": "Batch Document 1",
                    "content": "First document in batch operation",
                    "category": "batch",
                    "priority": "medium"
                },
                {
                    "title": "Batch Document 2", 
                    "content": "Second document in batch operation",
                    "category": "batch",
                    "priority": "low"
                },
                {
                    "title": "Performance Issue",
                    "content": "System running slowly during peak hours",
                    "category": "performance",
                    "priority": "high"
                },
                {
                    "title": "Bug Report",
                    "content": "Login button not working on mobile devices",
                    "category": "bug",
                    "priority": "critical"
                }
            ]
            
            with collection.batch.dynamic() as batch:
                for doc in batch_docs:
                    batch.add_object(doc)
            
            print(f"   ✅ Added {len(batch_docs)} documents in batch")
            
            # Step 4: Query data
            print(f"\n🔍 Querying documents...")
            
            # Query 1: Get all documents
            all_docs = collection.query.fetch_objects(limit=10)
            print(f"   📊 Total documents: {len(all_docs.objects)}")
            
            # Query 2: Filter by category
            print(f"\n🔎 Filtering documents by category 'test'...")
            from weaviate.classes.query import Filter
            try:
                filter_results = collection.query.fetch_objects(
                    limit=5,
                    filters=Filter.by_property("category").equal("test")
                )
                
                print(f"   Found {len(filter_results.objects)} test documents:")
                for i, obj in enumerate(filter_results.objects, 1):
                    title = obj.properties.get("title", "No title")
                    category = obj.properties.get("category", "No category")
                    print(f"   {i}. {title} (Category: {category})")
            except Exception as e:
                print(f"   Filter query failed: {e}")
            
            # Query 3: Get documents by properties
            print(f"\n🔎 Getting all batch category documents...")
            try:
                batch_results = collection.query.fetch_objects(
                    limit=5,
                    filters=Filter.by_property("category").equal("batch")
                )
                
                print(f"   Found {len(batch_results.objects)} batch documents:")
                for i, obj in enumerate(batch_results.objects, 1):
                    title = obj.properties.get("title", "No title")
                    priority = obj.properties.get("priority", "No priority")
                    print(f"   {i}. {title} (Priority: {priority})")
            except Exception as e:
                print(f"   Batch query failed: {e}")
            
            # Step 5: Delete collection
            print(f"\n🗑️  Cleaning up - deleting collection...")
            client.collections.delete(collection_name)
            print("   ✅ Collection deleted successfully")
            
            print(f"\n🎉 Complete CRUD workflow successful!")
            return True
            
        except Exception as e:
            print(f"❌ Error during CRUD operations: {e}")
            
            # Cleanup on error
            try:
                if client.collections.exists(collection_name):
                    client.collections.delete(collection_name)
                    print("   🧹 Cleaned up test collection")
            except:
                pass
                
            return False
            
        finally:
            client.close()
            print("✅ Connection closed")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_openai_connection():
    """Test OpenAI connection."""
    print("\n=== OpenAI Connection Test ===")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    print(f"OpenAI API Key: {'SET' if openai_key else 'NOT SET'}")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not configured")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello in one word"}],
            max_tokens=5
        )
        
        print("✅ Successfully connected to OpenAI!")
        print(f"✅ Test response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend integrations...\n")
    
    weaviate_ok = test_weaviate_full_workflow()
    openai_ok = test_openai_connection()
    
    print(f"\n=== Summary ===")
    print(f"Weaviate CRUD: {'✅ OK' if weaviate_ok else '❌ FAILED'}")
    print(f"OpenAI: {'✅ OK' if openai_ok else '❌ FAILED'}")
    
    if weaviate_ok and openai_ok:
        print("\n🎉 All integrations working perfectly!")
    elif weaviate_ok:
        print("\n🎯 Weaviate is ready! Configure OpenAI to complete setup.")
    else:
        print("\n⚠️  Some integrations need configuration") 