#!/usr/bin/env python3
"""Test script for ticket creation and retrieval flow."""

import json
import time
import requests
import subprocess
import sys
import os
from typing import Optional
import signal
import threading
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

class APITestRunner:
    """Test runner for API endpoints."""
    
    def __init__(self, port: int = 8001):
        self.port = port
        self.base_url = f"http://localhost:{port}"
        self.server_process: Optional[subprocess.Popen] = None
        
    def start_server(self) -> bool:
        """Start the FastAPI server."""
        print("🚀 Starting FastAPI server...")
        
        # Change to backend directory
        backend_dir = Path(__file__).parent
        
        try:
            # Start the server process
            self.server_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", str(self.port)],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to be ready
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=2)
                    if response.status_code == 200:
                        print(f"✅ Server started successfully on port {self.port}")
                        return True
                except requests.exceptions.RequestException:
                    pass
                
                print(f"⏳ Waiting for server... (attempt {attempt + 1}/{max_attempts})")
                time.sleep(2)
            
            print("❌ Server failed to start within timeout")
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
    
    def stop_server(self):
        """Stop the FastAPI server."""
        if self.server_process:
            print("🛑 Stopping server...")
            self.server_process.terminate()
            
            # Wait for graceful shutdown
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("⚠️ Server didn't stop gracefully, killing...")
                self.server_process.kill()
                self.server_process.wait()
            
            print("✅ Server stopped")
    
    def test_health_endpoint(self) -> bool:
        """Test the health endpoint."""
        print("\n📊 Testing health endpoint...")
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_config_endpoint(self) -> bool:
        """Test the config endpoint."""
        print("\n⚙️ Testing config endpoint...")
        try:
            response = requests.get(f"{self.base_url}/config")
            print(f"Status: {response.status_code}")
            config = response.json()
            print(f"Config: {json.dumps(config, indent=2)}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Config check failed: {e}")
            return False
    
    def create_ticket(self, problem: str) -> Optional[dict]:
        """Create a new ticket."""
        print(f"\n🎫 Creating ticket with problem: '{problem}'")
        
        try:
            payload = {"problem": problem}
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                f"{self.base_url}/tickets/",
                json=payload,
                timeout=60  # AI generation can take time
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                ticket = response.json()
                print(f"✅ Ticket created successfully!")
                print(f"Ticket ID: {ticket['id']}")
                print(f"Response: {json.dumps(ticket, indent=2)}")
                return ticket
            else:
                print(f"❌ Failed to create ticket")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating ticket: {e}")
            return None
    
    def get_ticket(self, ticket_id: str) -> Optional[dict]:
        """Retrieve a ticket by ID."""
        print(f"\n🔍 Retrieving ticket: {ticket_id}")
        
        try:
            response = requests.get(f"{self.base_url}/tickets/{ticket_id}")
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                ticket = response.json()
                print(f"✅ Ticket retrieved successfully!")
                print(f"Retrieved ticket: {json.dumps(ticket, indent=2)}")
                return ticket
            else:
                print(f"❌ Failed to retrieve ticket")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving ticket: {e}")
            return None
    
    def list_tickets(self, limit: int = 10) -> Optional[dict]:
        """List tickets with pagination."""
        print(f"\n📋 Listing tickets (limit: {limit})")
        
        try:
            response = requests.get(f"{self.base_url}/tickets/", params={"limit": limit})
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Tickets listed successfully!")
                print(f"Found {len(result.get('tickets', []))} tickets")
                print(f"Response: {json.dumps(result, indent=2)}")
                return result
            else:
                print(f"❌ Failed to list tickets")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error listing tickets: {e}")
            return None


def main():
    """Run the complete test flow."""
    print("🧪 Starting Ticket API Test Flow")
    print("=" * 50)
    
    # Create test runner
    runner = APITestRunner()
    
    try:
        # Start server
        if not runner.start_server():
            print("❌ Failed to start server, aborting test")
            return
        
        # Test basic endpoints
        if not runner.test_health_endpoint():
            print("❌ Health check failed")
            return
            
        runner.test_config_endpoint()
        
        # Test ticket creation with a realistic problem
        realistic_problems = [
            "I can't log into my account even though I'm using the correct password. It keeps saying 'invalid credentials' but I just reset my password yesterday.",
            "My payment was charged but my booking was not confirmed. I received the charge notification but no booking confirmation email.",
            "The app keeps crashing when I try to view my reservations. It worked fine last week but now it crashes immediately.",
            "I need to cancel my booking for next week but the cancel button is not working. I need a refund ASAP.",
            "The property I booked looks nothing like the photos. The room is much smaller and dirty. I want to check out early."
        ]
        
        # Use the first problem for detailed testing
        test_problem = realistic_problems[0]
        
        # Create ticket
        ticket = runner.create_ticket(test_problem)
        if not ticket:
            print("❌ Ticket creation failed, aborting test")
            return
        
        ticket_id = ticket["id"]
        
        # Wait a moment
        print("\n⏳ Waiting 2 seconds before retrieval...")
        time.sleep(2)
        
        # Retrieve the ticket
        retrieved_ticket = runner.get_ticket(ticket_id)
        if not retrieved_ticket:
            print("❌ Ticket retrieval failed")
            return
        
        # List tickets
        tickets_list = runner.list_tickets()
        
        # Final summary
        print("\n" + "=" * 50)
        print("🎉 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        print(f"✅ Created ticket: {ticket_id}")
        print(f"✅ Problem: {test_problem}")
        print(f"✅ Generated solution: {ticket.get('solution', 'N/A')[:100]}...")
        print(f"✅ Category: {ticket.get('category', 'N/A')}")
        print(f"✅ Successfully retrieved ticket")
        print(f"✅ Listed tickets: {len(tickets_list.get('tickets', [])) if tickets_list else 0} found")
        
        print("\n🔍 FINAL TICKET DETAILS:")
        print(json.dumps(retrieved_ticket, indent=2))
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
    
    finally:
        # Always stop the server
        runner.stop_server()
        print("\n✅ Test completed")


if __name__ == "__main__":
    main() 