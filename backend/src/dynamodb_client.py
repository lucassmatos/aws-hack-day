"""DynamoDB client configuration."""

import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Optional, List, Dict, Any
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from .config import get_dynamodb_config, get_aws_config
from .ticket_types import Ticket

# Load environment variables
load_dotenv()


def create_dynamodb_client() -> Optional[boto3.resource]:
    """Create and return DynamoDB client."""
    aws_config = get_aws_config()
    
    if not aws_config:
        print("AWS credentials not configured")
        return None
    
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=aws_config["aws_access_key_id"],
            aws_secret_access_key=aws_config["aws_secret_access_key"],
            region_name=aws_config["region_name"]
        )
        
        return dynamodb
        
    except Exception as e:
        print(f"Error connecting to DynamoDB: {e}")
        return None


def get_table(client: boto3.resource, table_name: str) -> Optional[Any]:
    """Get DynamoDB table reference."""
    if not client:
        return None
        
    try:
        table = client.Table(table_name)
        # Test table exists by describing it
        table.load()
        return table
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table {table_name} does not exist")
        else:
            print(f"Error accessing table {table_name}: {e}")
        return None
    except Exception as e:
        print(f"Error getting table {table_name}: {e}")
        return None


def save_ticket(ticket: Ticket) -> bool:
    """Save ticket to DynamoDB."""
    client = create_dynamodb_client()
    if not client:
        return False
    
    config = get_dynamodb_config()
    if not config:
        print("DynamoDB configuration not found")
        return False
    
    table = get_table(client, config["table_name"])
    if not table:
        return False
    
    try:
        # Add timestamp for sorting/tracking
        from datetime import datetime
        ticket_item = {
            **ticket,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        table.put_item(Item=ticket_item)
        print(f"✅ Ticket {ticket['id']} saved successfully")
        return True
        
    except Exception as e:
        print(f"Error saving ticket: {e}")
        return False


def get_ticket_by_id(ticket_id: str) -> Optional[Ticket]:
    """Get single ticket by ID."""
    client = create_dynamodb_client()
    if not client:
        return None
    
    config = get_dynamodb_config()
    if not config:
        print("DynamoDB configuration not found")
        return None
    
    table = get_table(client, config["table_name"])
    if not table:
        return None
    
    try:
        response = table.get_item(Key={'id': ticket_id})
        
        if 'Item' not in response:
            print(f"Ticket {ticket_id} not found")
            return None
            
        return response['Item']
        
    except Exception as e:
        print(f"Error getting ticket {ticket_id}: {e}")
        return None


def list_tickets(limit: int = 50, page_token: Optional[Dict] = None) -> Dict[str, Any]:
    """List tickets with pagination support."""
    client = create_dynamodb_client()
    if not client:
        return {"tickets": [], "next_page_token": None}
    
    config = get_dynamodb_config()
    if not config:
        print("DynamoDB configuration not found")
        return {"tickets": [], "next_page_token": None}
    
    table = get_table(client, config["table_name"])
    if not table:
        return {"tickets": [], "next_page_token": None}
    
    try:
        # Build scan parameters
        scan_params: Dict[str, Any] = {"Limit": limit}
        if page_token:
            scan_params["ExclusiveStartKey"] = page_token
        
        response = table.scan(**scan_params)
        
        tickets = response.get('Items', [])
        next_page_token = response.get('LastEvaluatedKey')
        
        print(f"✅ Found {len(tickets)} tickets on this page")
        return {
            "tickets": tickets,
            "next_page_token": next_page_token
        }
        
    except Exception as e:
        print(f"Error listing tickets: {e}")
        return {"tickets": [], "next_page_token": None}


def query_tickets_by_category(category: str, limit: int = 20) -> List[Ticket]:
    """Query tickets by category."""
    client = create_dynamodb_client()
    if not client:
        return []
    
    config = get_dynamodb_config()
    if not config:
        print("DynamoDB configuration not found")
        return []
    
    table = get_table(client, config["table_name"])
    if not table:
        return []
    
    try:
        response = table.scan(
            FilterExpression=Attr('category').eq(category),
            Limit=limit
        )
        
        tickets = response.get('Items', [])
        print(f"✅ Found {len(tickets)} tickets in category {category}")
        return tickets
        
    except Exception as e:
        print(f"Error querying tickets by category {category}: {e}")
        return []


def create_table_if_not_exists() -> bool:
    """Create tickets table if it doesn't exist."""
    client = create_dynamodb_client()
    if not client:
        return False
    
    config = get_dynamodb_config()
    if not config:
        print("DynamoDB configuration not found")
        return False
    
    table_name = config["table_name"]
    
    try:
        # Check if table exists
        table = client.Table(table_name)
        table.load()
        print(f"✅ Table {table_name} already exists")
        return True
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # Table doesn't exist, create it
            try:
                print(f"📁 Creating table {table_name}...")
                
                table = client.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'id',
                            'KeyType': 'HASH'  # Partition key
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id',
                            'AttributeType': 'S'
                        }
                    ],
                    BillingMode='PAY_PER_REQUEST'  # On-demand pricing
                )
                
                # Wait for table to be created
                table.wait_until_exists()
                print(f"✅ Table {table_name} created successfully")
                return True
                
            except Exception as create_error:
                print(f"Error creating table {table_name}: {create_error}")
                return False
        else:
            print(f"Error checking table {table_name}: {e}")
            return False
    except Exception as e:
        print(f"Error accessing table {table_name}: {e}")
        return False


# Public API
dynamodb_client_api = {
    "create_dynamodb_client": create_dynamodb_client,
    "save_ticket": save_ticket,
    "get_ticket_by_id": get_ticket_by_id,
    "list_tickets": list_tickets,
    "query_tickets_by_category": query_tickets_by_category,
    "create_table_if_not_exists": create_table_if_not_exists,
} 