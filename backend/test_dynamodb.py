#!/usr/bin/env python3
"""Test DynamoDB client functionality."""

import asyncio
from src.dynamodb_client import (
    create_table_if_not_exists, 
    save_ticket, 
    get_ticket_by_id, 
    list_tickets,
    query_tickets_by_category
)
from src.openai_service import create_ticket_agent


async def test_dynamodb():
    """Test DynamoDB functionality."""
    print("=== DynamoDB Client Test ===\n")
    
    # Test 1: Create table
    print("1. Creating/verifying table...")
    if create_table_if_not_exists():
        print("✅ Table ready")
    else:
        print("❌ Table creation failed")
        return
    
    # Test 2: Create agent and generate ticket
    print("\n2. Creating ticket with agent...")
    agent = create_ticket_agent()
    
    try:
        ticket = await agent.create_ticket_with_solution("My payment failed")
        if not ticket or not isinstance(ticket, dict):
            print("❌ Failed to create ticket")
            return
            
        print(f"✅ Generated ticket: {ticket.get('id', 'unknown')}")
        print(f"   Problem: {ticket.get('problem', 'unknown')}")
        print(f"   Category: {ticket.get('category', 'unknown')}")
        solution = ticket.get('solution', '')
        if solution:
            print(f"   Solution: {solution[:100]}...")
    except Exception as e:
        print(f"❌ Error creating ticket: {e}")
        return
    
    # Test 3: Get ticket by ID
    print(f"\n3. Retrieving ticket {ticket['id']}...")
    retrieved = get_ticket_by_id(ticket['id'])
    if retrieved:
        print(f"✅ Retrieved: {retrieved['problem']}")
    else:
        print("❌ Failed to retrieve ticket")
    
    # Test 4: List all tickets
    print("\n4. Listing all tickets...")
    tickets = list_tickets(limit=10)
    print(f"✅ Found {len(tickets)} total tickets")
    
    for t in tickets[:3]:  # Show first 3
        print(f"   - {t['id']}: {t['category']}")
    
    # Test 5: Query by category
    print(f"\n5. Querying tickets in category '{ticket['category']}'...")
    category_tickets = query_tickets_by_category(ticket['category'])
    print(f"✅ Found {len(category_tickets)} tickets in this category")
    
    print("\n🎉 DynamoDB test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_dynamodb()) 