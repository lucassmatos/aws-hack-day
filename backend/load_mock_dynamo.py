#!/usr/bin/env python3
"""Load mock issues dataset into DynamoDB."""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from src.dynamodb_client import (
    create_table_if_not_exists,
    save_ticket,
    list_tickets
)
from src.ticket_types import Ticket

# Load environment variables
load_dotenv()


def load_mock_data_to_dynamodb():
    """Load mock issues dataset into DynamoDB."""
    print("=== Loading Mock Issues Dataset into DynamoDB ===")
    
    # Check if we can connect to DynamoDB
    print("\n🔗 Verifying DynamoDB connection...")
    if not create_table_if_not_exists():
        print("❌ Could not create/access DynamoDB table")
        return False
    
    print("✅ DynamoDB table ready")

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
    
    if not issues:
        print("❌ No issues to load")
        return False

    # Load data into DynamoDB
    print(f"\n📚 Loading {len(issues)} issues into DynamoDB...")
    
    success_count = 0
    batch_size = 10
    timestamp = datetime.utcnow().isoformat()
    
    for i, issue in enumerate(issues):
        try:
            # Convert issue to Ticket format
            ticket: Ticket = {
                "id": issue["id"],
                "problem": issue["problem"],
                "solution": issue["solution"],
                "category": issue["category"],
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            # Save to DynamoDB
            if save_ticket(ticket):
                success_count += 1
            else:
                print(f"   ⚠️  Failed to save issue {issue['id']}")
            
            # Progress indicator
            if (i + 1) % batch_size == 0:
                print(f"   📝 Processed {i + 1}/{len(issues)} issues...")
                
        except Exception as e:
            print(f"   ⚠️  Error processing issue {issue.get('id', 'unknown')}: {e}")
    
    print(f"   ✅ Successfully loaded {success_count}/{len(issues)} issues")
    
    # Verify the data
    print(f"\n🔍 Verifying loaded data...")
    tickets = list_tickets(limit=10)
    
    if tickets:
        print(f"   ✅ Verification successful - found {len(tickets)} sample tickets:")
        for i, ticket in enumerate(tickets[:3], 1):
            ticket_id = ticket.get("id", "Unknown")
            category = ticket.get("category", "Unknown")
            print(f"   {i}. {ticket_id} - {category}")
    else:
        print("   ⚠️  No tickets found after loading")
    
    # Show collection stats
    all_tickets = list_tickets(limit=1000)  # Get more for stats
    print(f"\n📊 DynamoDB Table Statistics:")
    print(f"   Table: tickets")
    print(f"   Total Tickets: {len(all_tickets)}")
    
    # Group by category
    categories = {}
    for ticket in all_tickets:
        cat = ticket.get("category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"   Categories:")
    for cat, count in categories.items():
        print(f"     - {cat}: {count} tickets")
    
    print(f"\n🎉 Data loading completed successfully!")
    return True


if __name__ == "__main__":
    print("Loading mock issues dataset into DynamoDB...\n")
    
    success = load_mock_data_to_dynamodb()
    
    print(f"\n=== Summary ===")
    if success:
        print("✅ Mock data loaded successfully into DynamoDB!")
        print("🔍 You can now query tickets from DynamoDB for the UI")
    else:
        print("❌ Data loading failed")
        print("💡 Check your AWS DynamoDB configuration and try again") 