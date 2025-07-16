#!/usr/bin/env python3
"""Update existing tickets to add entity_type field for GSI compatibility."""

from src.dynamodb_client import create_dynamodb_client, get_table
from src.config import get_dynamodb_config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_existing_tickets():
    """Add entity_type field to existing tickets for GSI compatibility."""
    print("=== Updating Existing Tickets for GSI Compatibility ===")
    
    client = create_dynamodb_client()
    if not client:
        print("❌ Could not create DynamoDB client")
        return False
    
    config = get_dynamodb_config()
    if not config:
        print("❌ DynamoDB configuration not found")
        return False
    
    table = get_table(client, config["table_name"])
    if not table:
        print("❌ Could not get table")
        return False
    
    try:
        print(f"📋 Scanning table: {config['table_name']}")
        
        # Scan all items in the table
        response = table.scan()
        items = response.get('Items', [])
        
        # Handle pagination if needed
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
        
        print(f"📊 Found {len(items)} total items in table")
        
        # Filter items that don't have entity_type
        items_to_update = []
        for item in items:
            if 'entity_type' not in item:
                items_to_update.append(item)
        
        print(f"🔄 {len(items_to_update)} items need entity_type field added")
        
        if len(items_to_update) == 0:
            print("✅ All items already have entity_type field!")
            return True
        
        # Update items in batches
        batch_size = 25  # DynamoDB batch write limit
        updated_count = 0
        
        for i in range(0, len(items_to_update), batch_size):
            batch = items_to_update[i:i + batch_size]
            
            print(f"📝 Updating batch {i//batch_size + 1} ({len(batch)} items)...")
            
            # Prepare batch write request
            with table.batch_writer() as batch_writer:
                for item in batch:
                    # Add entity_type field
                    item['entity_type'] = 'TICKET'
                    
                    # Write the updated item
                    batch_writer.put_item(Item=item)
                    updated_count += 1
            
            print(f"   ✅ Updated {len(batch)} items")
        
        print(f"🎉 Successfully updated {updated_count} tickets with entity_type field!")
        print("✅ All tickets are now compatible with the CreatedAtIndex GSI")
        return True
        
    except Exception as e:
        print(f"❌ Error updating tickets: {e}")
        return False

if __name__ == "__main__":
    print("Updating existing tickets for GSI compatibility...\n")
    
    success = update_existing_tickets()
    
    if success:
        print("\n🎉 Ticket update completed!")
        print("💡 Now you can use the GSI for efficient sorting!")
        print("💡 Test with: python3 -c \"from src.dynamodb_client import list_tickets; result = list_tickets(limit=3); print(f'Method used: GSI' if 'GSI' in str(result) else 'Fallback')\"")
    else:
        print("\n❌ Ticket update failed")
        print("💡 Check your AWS credentials and table configuration") 