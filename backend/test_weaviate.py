#!/usr/bin/env python3
"""Simple test for Weaviate integration."""

import sys
import os
from dotenv import load_dotenv

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from weviate_service import create_weviate_service
from openai_service import create_openai_service

# Load environment variables
load_dotenv()

def test_weaviate():
    """Test Weaviate service connection and basic operations."""
    print("=== Weaviate Integration Test ===")
    
    # Test OpenAI Service
    print("\n🤖 Testing OpenAI Service...")
    openai_service = create_openai_service()
    if openai_service.connect():
        print("✅ Connected to OpenAI")
        try:
            response = openai_service.generate_text("Say hello!", max_tokens=50)
            print(f"✅ AI Response: {response}")
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
    else:
        print("❌ Failed to connect to OpenAI (check OPENAI_API_KEY)")
    
    # Test Weaviate Service
    print("\n🔍 Testing Weaviate Service...")
    service = create_weviate_service("Documents")  # Use a generic collection name
    
    if service.connect():
        print("✅ Connected to Weaviate")
        
        try:
            # Test adding a document
            document = {
                "id": "test_001",
                "title": "Test Document",
                "description": "This is a test document for integration testing",
                "category": "test"
            }
            
            if service.add_document(document):
                print("✅ Document added successfully")
            else:
                print("❌ Failed to add document")
            
            # Test querying
            results = service.query("test document", limit=3)
            print(f"✅ Query successful - found {len(results)} results")
            
            for ticket in results:
                print(f"   - {ticket['id']}: {ticket['description']}")
                
        except Exception as e:
            print(f"❌ Weaviate operation error: {e}")
        
        finally:
            service.disconnect()
            print("✅ Disconnected from Weaviate")
        
    else:
        print("❌ Failed to connect to Weaviate")
        print("   Check your WEAVIATE_URL and WEAVIATE_API_KEY in .env file")
        print("   Make sure your Weaviate cluster is running")

if __name__ == "__main__":
    test_weaviate() 