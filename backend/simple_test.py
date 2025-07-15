#!/usr/bin/env python3
"""Simple Weaviate connection test."""

import os
import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_weaviate_connection():
    """Test basic Weaviate connection."""
    print("=== Simple Weaviate Connection Test ===")
    
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
        print("\n🔗 Attempting to connect to Weaviate...")
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_key),
        )
        
        if client.is_ready():
            print("✅ Successfully connected to Weaviate!")
            
            # Test basic functionality
            try:
                # List collections
                collections = client.collections.list_all()
                print(f"✅ Found {len(collections)} collections")
                
                if collections:
                    print("Collections:")
                    for collection in collections:
                        print(f"   - {collection}")
                else:
                    print("   No collections found")
                    
            except Exception as e:
                print(f"⚠️  Connected but error listing collections: {e}")
            
            finally:
                client.close()
                print("✅ Connection closed")
                
            return True
        else:
            print("❌ Connected but Weaviate is not ready")
            return False
            
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
            model="gpt-3.5-turbo",
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
    
    weaviate_ok = test_weaviate_connection()
    openai_ok = test_openai_connection()
    
    print(f"\n=== Summary ===")
    print(f"Weaviate: {'✅ OK' if weaviate_ok else '❌ FAILED'}")
    print(f"OpenAI: {'✅ OK' if openai_ok else '❌ FAILED'}")
    
    if weaviate_ok and openai_ok:
        print("\n🎉 All integrations working!")
    else:
        print("\n⚠️  Some integrations need configuration") 