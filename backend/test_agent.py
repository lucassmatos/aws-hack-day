#!/usr/bin/env python3
"""Test script for the OpenAI agents-based ticket agent."""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_service import create_ticket_agent

# Load environment variables
load_dotenv()


async def test_ticket_agent():
    """Test the ticket agent with various customer problems."""
    print("=== OpenAI Agents Ticket Agent Test ===\n")
    
    # Create the agent
    agent = create_ticket_agent()
    
    # Test problems
    test_problems = [
        "I can't log into my account, it says my password is wrong",
        "My payment was declined but I know my card is good",
        "The host isn't responding to my messages", 
        "I want to cancel my booking but need a refund",
        "The app keeps crashing when I try to view my bookings"
    ]
    
    for i, problem in enumerate(test_problems, 1):
        print(f"🎫 Test {i}: {problem}")
        print("-" * 60)
        
        try:
            # Generate solution using the agent
            solution = await agent.generate_solution(problem)
            print(f"💡 Solution:\n{solution}\n")
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    print("🎉 Test completed!")


async def interactive_agent():
    """Run the agent in interactive mode."""
    print("🤖 Interactive Ticket Agent")
    print("Type your customer problems (or 'quit' to exit):\n")
    
    agent = create_ticket_agent()
    
    while True:
        try:
            problem = input("Customer Problem > ").strip()
            
            if problem.lower() in ['quit', 'exit', 'q']:
                break
                
            if not problem:
                print("Please enter a customer problem")
                continue
            
            print("\n🤖 Agent is working...\n")
            solution = await agent.generate_solution(problem)
            print(f"💡 Solution:\n{solution}\n")
            print("-" * 60)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")
            
    print("\n👋 Goodbye!")


async def create_full_ticket_demo():
    """Demonstrate creating a complete ticket with solution."""
    print("=== Full Ticket Creation Demo ===\n")
    
    agent = create_ticket_agent()
    
    problem = "I booked a cabin but never received confirmation email and my payment went through"
    
    print(f"Creating ticket for: {problem}\n")
    
    try:
        ticket = await agent.create_ticket_with_solution(problem)
        
        print("✅ Ticket created successfully!")
        print(f"📋 Ticket ID: {ticket['id']}")
        print(f"🔧 Problem: {ticket['problem']}")
        print(f"💡 Solution: {ticket['solution']}")
        
    except Exception as e:
        print(f"❌ Error creating ticket: {e}")


if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Run predefined tests")
    print("2. Interactive mode") 
    print("3. Full ticket creation demo")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        asyncio.run(test_ticket_agent())
    elif choice == "2":
        asyncio.run(interactive_agent())
    elif choice == "3":
        asyncio.run(create_full_ticket_demo())
    else:
        print("Invalid choice. Running default test...")
        asyncio.run(test_ticket_agent()) 