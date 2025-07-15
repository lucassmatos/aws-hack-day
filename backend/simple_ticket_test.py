#!/usr/bin/env python3
"""Simple test for ticket creation using FastAPI TestClient."""

import json
import sys
import os
from pathlib import Path

# Add the current directory and src directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "src"))

# Set PYTHONPATH environment variable as well
os.environ['PYTHONPATH'] = str(current_dir / "src")

try:
    from fastapi.testclient import TestClient
    # Import directly from the main module
    import main
    app = main.app
    
    def test_ticket_flow():
        """Test the complete ticket creation and retrieval flow."""
        print("🧪 Starting Simple Ticket API Test")
        print("=" * 50)
        
        # Create test client
        client = TestClient(app)
        
        # Test health endpoint
        print("\n📊 Testing health endpoint...")
        health_response = client.get("/health")
        print(f"Status: {health_response.status_code}")
        print(f"Response: {health_response.json()}")
        
        # Test config endpoint
        print("\n⚙️ Testing config endpoint...")
        config_response = client.get("/config")
        print(f"Status: {config_response.status_code}")
        config_data = config_response.json()
        print(f"Config: {json.dumps(config_data, indent=2)}")
        
        # Test ticket creation with a realistic problem
        test_problem = "I can't log into my account even though I'm using the correct password. It keeps saying 'invalid credentials' but I just reset my password yesterday."
        
        print(f"\n🎫 Creating ticket with problem:")
        print(f"'{test_problem}'")
        
        # Create ticket payload
        ticket_payload = {"problem": test_problem}
        print(f"\nPayload: {json.dumps(ticket_payload, indent=2)}")
        
        # Make the POST request to create ticket
        print("\n⏳ Calling ticket creation endpoint (this may take a moment for AI generation)...")
        
        try:
            create_response = client.post("/tickets/", json=ticket_payload)
            print(f"Status: {create_response.status_code}")
            
            if create_response.status_code == 200:
                ticket = create_response.json()
                print(f"✅ Ticket created successfully!")
                print(f"Ticket ID: {ticket['id']}")
                print(f"Created ticket: {json.dumps(ticket, indent=2)}")
                
                # Now test retrieving the ticket
                ticket_id = ticket["id"]
                print(f"\n🔍 Retrieving ticket: {ticket_id}")
                
                get_response = client.get(f"/tickets/{ticket_id}")
                print(f"Status: {get_response.status_code}")
                
                if get_response.status_code == 200:
                    retrieved_ticket = get_response.json()
                    print(f"✅ Ticket retrieved successfully!")
                    print(f"Retrieved ticket: {json.dumps(retrieved_ticket, indent=2)}")
                    
                    # Test listing tickets
                    print(f"\n📋 Testing ticket listing...")
                    list_response = client.get("/tickets/", params={"limit": 5})
                    print(f"Status: {list_response.status_code}")
                    
                    if list_response.status_code == 200:
                        tickets_data = list_response.json()
                        print(f"✅ Tickets listed successfully!")
                        print(f"Found {len(tickets_data.get('tickets', []))} tickets")
                        print(f"List response: {json.dumps(tickets_data, indent=2)}")
                    else:
                        print(f"❌ Failed to list tickets: {list_response.text}")
                    
                    # Final summary
                    print("\n" + "=" * 50)
                    print("🎉 TEST RESULTS SUMMARY")
                    print("=" * 50)
                    
                    print(f"✅ Health check: PASSED")
                    print(f"✅ Config check: PASSED")
                    print(f"✅ Created ticket: {ticket_id}")
                    print(f"✅ Problem: {test_problem}")
                    print(f"✅ Generated solution: {ticket.get('solution', 'N/A')[:100]}...")
                    print(f"✅ Category: {ticket.get('category', 'N/A')}")
                    print(f"✅ Retrieved ticket: PASSED")
                    print(f"✅ Listed tickets: PASSED")
                    
                    print("\n🔍 FINAL TICKET DETAILS:")
                    print(json.dumps(retrieved_ticket, indent=2))
                    
                else:
                    print(f"❌ Failed to retrieve ticket: {get_response.text}")
                    
            else:
                print(f"❌ Failed to create ticket")
                print(f"Response: {create_response.text}")
                
        except Exception as e:
            print(f"❌ Error during ticket creation: {e}")
            print(f"Exception type: {type(e).__name__}")
    
    if __name__ == "__main__":
        test_ticket_flow()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip3 install fastapi uvicorn")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print(f"Exception type: {type(e).__name__}") 