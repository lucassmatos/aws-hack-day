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

    # Load all JSON files from mock-issues directory
    mock_issues_dir = "../docs-and-mock-data/mock-issues"
    if not os.path.exists(mock_issues_dir):
        print(f"\n❌ Mock issues directory not found: {mock_issues_dir}")
        return False
    
    print(f"\n📂 Loading datasets from: {mock_issues_dir}")
    
    # List of JSON files to load
    json_files = [
        "booking-reservation-issues.json",
        "payment-billing-issues.json",
        "property-stay-issues.json",
        "host-seller-issues.json",
        "technical-app-issues.json"
    ]
    
    # Collect all issues from all files
    all_issues = []
    
    for json_file in json_files:
        file_path = os.path.join(mock_issues_dir, json_file)
        if os.path.exists(file_path):
            print(f"   📄 Loading {json_file}...")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_issues = json.load(f)
                print(f"      ✅ Found {len(file_issues)} issues")
                all_issues.extend(file_issues)
            except Exception as e:
                print(f"      ❌ Error reading {json_file}: {e}")
        else:
            print(f"   ⚠️  File not found: {json_file}")
    
    issues = all_issues
    print(f"\n✅ Total issues loaded: {len(issues)} from {len(json_files)} files")

    # Get OpenAI API key for vectorizer
    openai_key = os.getenv("OPENAI_API_KEY")
    print(f"OpenAI API Key: {'SET' if openai_key else 'NOT SET'}")

    try:
        print("\n🔗 Connecting to Weaviate...")
        # Set environment variables for Weaviate
        if openai_key:
            os.environ["OPENAI_APIKEY"] = openai_key
            os.environ["X-OPENAI-API-KEY"] = openai_key
        
        headers = {"X-Openai-Api-Key": openai_key} if openai_key else {}
        
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_key),
            headers=headers
        )
        
        if not client.is_ready():
            print("❌ Weaviate is not ready")
            return False
            
        print("✅ Connected to Weaviate!")
        
        # Collection name for the issues
        collection_name = "Tickets"
        
        try:
            # Step 1: Use existing collection 
            print(f"\n📁 Using existing collection '{collection_name}'...")
            
            if client.collections.exists(collection_name):
                print(f"   ✅ Collection exists, using it")
                collection = client.collections.get(collection_name)
            else:
                print(f"   ❌ Collection '{collection_name}' not found")
                print("   Please create the collection manually first")
                return False
            
            # Step 2: Load data in batches
            print(f"\n📚 Loading {len(issues)} issues into Weaviate...")
            
            # Fresh collection, so no need to clear data
            print("   ℹ️  Loading data into fresh collection")
            
            # Batch insert the issues
            batch_size = 50
            success_count = 0
            error_count = 0
            
            try:
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
                            error_count += 1
                            print(f"   ⚠️  Error processing issue {issue.get('id', 'unknown')}: {e}")
                
                # Check for batch errors
                if hasattr(collection.batch, 'failed_objects') and collection.batch.failed_objects:
                    failed_count = len(collection.batch.failed_objects)
                    error_count += failed_count
                    print(f"   ⚠️  {failed_count} objects failed during batch insertion")
                    
            except Exception as batch_error:
                print(f"   ❌ Batch operation failed: {batch_error}")
                error_count += 1
            
            print(f"   ✅ Successfully loaded {success_count}/{len(issues)} issues")
            if error_count > 0:
                print(f"   ⚠️  {error_count} errors occurred during loading")
            
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