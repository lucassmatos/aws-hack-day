#!/usr/bin/env python3
"""Manual API test - run this while the server is running."""

import requests
import json
import time

def test_running_api():
    """Test the API if it's running."""
    base_url = "http://localhost:8000"
    
    print("🧪 Manual API Test - Server should be running")
    print("=" * 50)
    print("To start server: uvicorn src.main:app --reload")
    print("=" * 50)
    
    try:
        # Test health
        print("\n📊 Testing health endpoint...")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Status: {health_response.status_code}")
        print(f"Response: {health_response.json()}")
        
        # Test config
        print("\n⚙️ Testing config endpoint...")
        config_response = requests.get(f"{base_url}/config", timeout=5)
        print(f"Status: {config_response.status_code}")
        config_data = config_response.json()
        print(f"Config: {json.dumps(config_data, indent=2)}")
        
        # Create ticket
        test_problem = "My payment was charged but my booking was not confirmed. I received the charge notification but no booking confirmation email."
        
        print(f"\n🎫 Creating ticket...")
        print(f"Problem: {test_problem}")
        
        ticket_payload = {"problem": test_problem}
        print(f"Payload: {json.dumps(ticket_payload, indent=2)}")
        
        create_response = requests.post(
            f"{base_url}/tickets/",
            json=ticket_payload,
            timeout=120  # AI can take time
        )
        
        print(f"Status: {create_response.status_code}")
        
        if create_response.status_code == 200:
            ticket = create_response.json()
            print(f"✅ Ticket created!")
            print(f"Created ticket: {json.dumps(ticket, indent=2)}")
            
            ticket_id = ticket["id"]
            
            # Get ticket
            print(f"\n🔍 Getting ticket {ticket_id}...")
            get_response = requests.get(f"{base_url}/tickets/{ticket_id}", timeout=10)
            
            if get_response.status_code == 200:
                retrieved_ticket = get_response.json()
                print(f"✅ Retrieved ticket!")
                print(f"Retrieved: {json.dumps(retrieved_ticket, indent=2)}")
                
                # List tickets
                print(f"\n📋 Listing tickets...")
                list_response = requests.get(f"{base_url}/tickets/", params={"limit": 3}, timeout=10)
                
                if list_response.status_code == 200:
                    tickets_data = list_response.json()
                    print(f"✅ Listed tickets!")
                    print(f"Found {len(tickets_data.get('tickets', []))} tickets")
                    
                    print(f"\n🎉 FULL TEST SUCCESS!")
                    print(f"✅ Health check: PASSED")
                    print(f"✅ Config check: PASSED") 
                    print(f"✅ Ticket creation: PASSED")
                    print(f"✅ Ticket retrieval: PASSED")
                    print(f"✅ Ticket listing: PASSED")
                    
                    print(f"\n🔍 FINAL TICKET DETAILS:")
                    print(json.dumps(retrieved_ticket, indent=2))
                    
                else:
                    print(f"❌ List failed: {list_response.text}")
            else:
                print(f"❌ Get failed: {get_response.text}")
        else:
            print(f"❌ Create failed: {create_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        print("Please start the server with: uvicorn src.main:app --reload")
    except requests.exceptions.Timeout:
        print("❌ Request timed out - AI generation may be taking longer")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_running_api() 