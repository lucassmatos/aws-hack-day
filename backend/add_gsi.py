#!/usr/bin/env python3
"""Add CreatedAtIndex GSI to existing DynamoDB table."""

import boto3
from dotenv import load_dotenv
from src.config import get_dynamodb_config, get_aws_config

# Load environment variables
load_dotenv()

def add_gsi_to_existing_table():
    """Add CreatedAtIndex GSI to existing tickets table."""
    print("=== Adding CreatedAtIndex GSI to Existing Table ===")
    
    # Get configurations
    aws_config = get_aws_config()
    dynamodb_config = get_dynamodb_config()
    
    if not aws_config or not dynamodb_config:
        print("❌ AWS or DynamoDB configuration not found")
        return False
    
    table_name = dynamodb_config["table_name"]
    
    try:
        # Create DynamoDB client
        dynamodb = boto3.client(
            'dynamodb',
            aws_access_key_id=aws_config["aws_access_key_id"],
            aws_secret_access_key=aws_config["aws_secret_access_key"],
            region_name=aws_config["region_name"]
        )
        
        print(f"🔗 Connected to DynamoDB")
        print(f"📋 Table: {table_name}")
        
        # Check if GSI already exists
        try:
            response = dynamodb.describe_table(TableName=table_name)
            table_description = response['Table']
            
            existing_gsis = table_description.get('GlobalSecondaryIndexes', [])
            for gsi in existing_gsis:
                if gsi['IndexName'] == 'CreatedAtIndex':
                    print("✅ GSI 'CreatedAtIndex' already exists!")
                    return True
            
        except Exception as e:
            print(f"❌ Error checking table: {e}")
            return False
        
        print("📝 GSI 'CreatedAtIndex' not found, adding it...")
        
        # Add the GSI
        try:
            response = dynamodb.update_table(
                TableName=table_name,
                AttributeDefinitions=[
                    {
                        'AttributeName': 'entity_type',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'created_at',
                        'AttributeType': 'S'
                    }
                ],
                GlobalSecondaryIndexUpdates=[
                    {
                        'Create': {
                            'IndexName': 'CreatedAtIndex',
                            'KeySchema': [
                                {
                                    'AttributeName': 'entity_type',
                                    'KeyType': 'HASH'
                                },
                                {
                                    'AttributeName': 'created_at',
                                    'KeyType': 'RANGE'
                                }
                            ],
                            'Projection': {
                                'ProjectionType': 'ALL'
                            }
                        }
                    }
                ]
            )
            
            print("✅ GSI creation initiated successfully!")
            print("⏳ GSI is being created... This may take a few minutes.")
            print("💡 You can check the status in the AWS Console or wait for completion.")
            
            # Optionally wait for the GSI to become active
            print("\n🔄 Waiting for GSI to become active...")
            waiter = dynamodb.get_waiter('table_exists')
            waiter.wait(TableName=table_name)
            
            # Check final status
            response = dynamodb.describe_table(TableName=table_name)
            table_description = response['Table']
            
            gsi_status = None
            for gsi in table_description.get('GlobalSecondaryIndexes', []):
                if gsi['IndexName'] == 'CreatedAtIndex':
                    gsi_status = gsi['IndexStatus']
                    break
            
            if gsi_status == 'ACTIVE':
                print("🎉 GSI 'CreatedAtIndex' is now ACTIVE!")
                print("✅ Your tickets will now be sorted efficiently using the GSI!")
            else:
                print(f"📊 GSI status: {gsi_status}")
                print("⏳ GSI may still be creating. Check AWS Console for progress.")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating GSI: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error connecting to DynamoDB: {e}")
        return False

if __name__ == "__main__":
    print("Adding CreatedAtIndex GSI to DynamoDB table...\n")
    
    success = add_gsi_to_existing_table()
    
    if success:
        print("\n🎉 GSI addition completed!")
        print("💡 Now test with: python3 -c \"from src.dynamodb_client import list_tickets; print(list_tickets(limit=3))\"")
    else:
        print("\n❌ GSI addition failed")
        print("💡 Check your AWS credentials and table configuration") 