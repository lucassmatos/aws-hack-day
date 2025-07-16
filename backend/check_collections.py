#!/usr/bin/env python3
"""Check object counts in all Weaviate collections."""

import os
import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv

load_dotenv()

def check_collections():
    """Check object counts in all collections."""
    print("=== Checking Weaviate Collections ===")
    
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_key = os.getenv("WEAVIATE_API_KEY")
    
    if not weaviate_url or not weaviate_key:
        print("❌ Weaviate credentials not configured")
        return
    
    try:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_key)
        )
        
        print(f"✅ Connected to Weaviate")
        
        collections = client.collections.list_all()
        print(f"\n📋 Found {len(collections)} collections:")
        
        for name in collections:
            try:
                collection = client.collections.get(name)
                objects = collection.query.fetch_objects(limit=1000)
                count = len(objects.objects)
                print(f"   📊 {name}: {count} objects")
                
                # Show a sample object if exists
                if count > 0:
                    sample = objects.objects[0]
                    props = list(sample.properties.keys())[:3]
                    print(f"      Sample properties: {props}")
                
            except Exception as e:
                print(f"   ❌ Error checking {name}: {e}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    check_collections() 