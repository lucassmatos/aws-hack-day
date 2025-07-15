#!/usr/bin/env python3
"""Load mock issues dataset into Weaviate."""

import os
import json
import weaviate
import weaviate.classes as wvc
from weaviate.classes.init import Auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_mock_data():
    """Load mock issues dataset into Weaviate."""
    print("=== Loading Mock Issues Dataset ===")
    
    # Get environment variables
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_key = os.getenv("WEAVIATE_API_KEY")
    
    print(f"Weaviate URL: {weaviate_url if weaviate_url else 'NOT SET'}")
    print(f"API Key: {'SET' if weaviate_key else 'NOT SET'}")
    
    if not weaviate_url or not weaviate_key:
        print("\n❌ WEAVIATE_URL or WEAVIATE_API_KEY not configured")
        print("   Create a .env file with your Weaviate credentials")
        return False

    # Load the dataset
    dataset_path = "../docs-and-mock-data/mock-issues-dataset.json"
    if not os.path.exists(dataset_path):
        print(f"\n❌ Dataset file not found: {dataset_path}")
        return False
    
    print(f"\n📂 Loading dataset from: {dataset_path}")
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        issues = data.get('issues', [])
        print(f"✅ Found {len(issues)} issues in dataset")
    except Exception as e:
        print(f"❌ Error reading dataset: {e}")
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
        
        # Collection name for the issues
        collection_name = "Tickets"
        
        try:
            # Step 1: Create Collection (if not exists)
            print(f"\n📁 Setting up collection '{collection_name}'...")
            
            if client.collections.exists(collection_name):
                print(f"   Collection already exists")
                collection = client.collections.get(collection_name)
            else:
                print(f"   Creating new collection without vectorization...")
                client.collections.create(
                    name=collection_name,
                    description="Customer support issues and solutions dataset",
                    vectorizer_config=wvc.config.Configure.Vectorizer.none()
                )
                collection = client.collections.get(collection_name)
                print("   ✅ Collection created successfully")
            
            # Step 2: Load data in batches
            print(f"\n📚 Loading {len(issues)} issues into Weaviate...")
            
            # Clear existing data (optional - skipped for now)
            print("   ℹ️  Adding to existing data (not clearing)")
            
            # Batch insert the issues
            batch_size = 10
            success_count = 0
            
            with collection.batch.dynamic() as batch:
                for i, issue in enumerate(issues):
                    try:
                        # Prepare the object
                        obj = {
                            "issue_id": issue["id"],
                            "category": issue["category"],
                            "problem": issue["problem"],
                            "solution": issue["solution"]
                        }
                        
                        # Add to batch
                        batch.add_object(obj)
                        success_count += 1
                        
                        # Progress indicator
                        if (i + 1) % batch_size == 0:
                            print(f"   📝 Processed {i + 1}/{len(issues)} issues...")
                            
                    except Exception as e:
                        print(f"   ⚠️  Error processing issue {issue.get('id', 'unknown')}: {e}")
            
            print(f"   ✅ Successfully loaded {success_count}/{len(issues)} issues")
            
            # Step 3: Verify the data
            print(f"\n🔍 Verifying loaded data...")
            result = collection.query.fetch_objects(limit=5)
            
            if result.objects:
                print(f"   ✅ Verification successful - found {len(result.objects)} sample objects:")
                for i, obj in enumerate(result.objects[:3], 1):
                    issue_id = obj.properties.get("issue_id", "Unknown")
                    category = obj.properties.get("category", "Unknown")
                    print(f"   {i}. {issue_id} - {category}")
            else:
                print("   ⚠️  No objects found after loading")
            
            # Step 4: Show collection stats
            total_result = collection.query.fetch_objects(limit=1000)  # Get count
            print(f"\n📊 Collection Statistics:")
            print(f"   Collection: {collection_name}")
            print(f"   Total Issues: {len(total_result.objects)}")
            
            # Group by category
            categories = {}
            for obj in total_result.objects:
                cat = obj.properties.get("category", "Unknown")
                categories[cat] = categories.get(cat, 0) + 1
            
            print(f"   Categories:")
            for cat, count in categories.items():
                print(f"     - {cat}: {count} issues")
            
            print(f"\n🎉 Data loading completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during data loading: {e}")
            return False
            
        finally:
            client.close()
            print("✅ Connection closed")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Loading mock issues dataset into Weaviate...\n")
    
    success = load_mock_data()
    
    print(f"\n=== Summary ===")
    if success:
        print("✅ Mock data loaded successfully!")
        print("🔍 You can now test queries against the SupportIssues collection")
    else:
        print("❌ Data loading failed")
        print("💡 Check your Weaviate configuration and try again") 