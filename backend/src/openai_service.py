"""OpenAI service for AI operations."""

import os
import json
import uuid
import asyncio
from typing import Optional, Dict, Any, List, TypedDict
from openai import OpenAI
import weaviate
from weaviate.classes.init import Auth
from config import get_openai_config, get_weaviate_config

# OpenAI agents imports
from agents import Agent, Runner, function_tool


class Ticket(TypedDict):
    """Ticket type definition."""
    id: str
    problem: str
    solution: Optional[str]


class OpenAIService:
    """Service for handling OpenAI operations."""
    
    def __init__(self):
        """Initialize OpenAI service."""
        self.client: Optional[OpenAI] = None
        self.config = get_openai_config()
    
    def connect(self) -> bool:
        """Connect to OpenAI."""
        if not self.config:
            print("OpenAI API key not configured")
            return False
        
        try:
            self.client = OpenAI(api_key=self.config["api_key"])
            return True
        except Exception as e:
            print(f"Error connecting to OpenAI: {e}")
            return False
    
    def generate_text(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Generate text using OpenAI."""
        if not self.client:
            return "OpenAI client not connected"
        
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens or self.config["max_tokens"]
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""
    
    def generate_embedding(self, text: str) -> list:
        """Generate embedding for text."""
        if not self.client:
            return []
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []


# Global Weaviate client
_weaviate_client: Optional[weaviate.WeaviateClient] = None


def _get_weaviate_client() -> Optional[weaviate.WeaviateClient]:
    """Get or create Weaviate client."""
    global _weaviate_client
    
    if _weaviate_client is None:
        config = get_weaviate_config()
        if not config:
            return None
            
        try:
            _weaviate_client = weaviate.connect_to_weaviate_cloud(
                cluster_url=config["url"],
                auth_credentials=Auth.api_key(config["api_key"]),
            )
            
            if not _weaviate_client.is_ready():
                return None
                
        except Exception as e:
            print(f"Error connecting to Weaviate: {e}")
            return None
    
    return _weaviate_client


# Relevance Evaluator Agent
relevance_agent = Agent(
    name="Relevance Evaluator",
    instructions="""You are a relevance evaluator. Given a customer problem and a list of support tickets, determine which tickets are actually relevant to solving the customer's problem.

Be strict - only return IDs of tickets that would genuinely help solve the customer's specific issue. Ignore tickets that are only tangentially related or about different problems entirely.

Return your response as a JSON object with this exact format:
{
    "relevant_ids": ["ID1", "ID2", "ID3"],
    "reasoning": "Brief explanation of your filtering decisions"
}""",
    tools=[],
)


@function_tool
async def get_all_tickets() -> str:
    """Get all tickets from the knowledge base.
    
    Returns:
        JSON string with all tickets
    """
    client = _get_weaviate_client()
    if not client:
        return json.dumps([])
    
    try:
        collection = client.collections.get("Tickets")
        response = collection.query.fetch_objects(limit=50)
        
        if not response.objects:
            return json.dumps([])
        
        # Convert to list
        all_tickets = []
        for obj in response.objects:
            all_tickets.append({
                "id": str(obj.properties.get("issue_id", "")),
                "problem": str(obj.properties.get("problem", "")),
                "solution": str(obj.properties.get("solution", ""))
            })
        
        return json.dumps(all_tickets)
        
    except Exception as e:
        print(f"Error getting tickets: {e}")
        return json.dumps([])


@function_tool
async def filter_relevant_tickets(customer_problem: str, all_tickets_json: str) -> str:
    """Filter tickets for relevance to customer problem.
    
    Args:
        customer_problem: The customer's problem description
        all_tickets_json: JSON string with all tickets
        
    Returns:
        JSON string with only relevant ticket IDs
    """
    try:
        tickets = json.loads(all_tickets_json)
        if not tickets:
            return json.dumps({"relevant_ids": [], "reasoning": "No tickets available"})
        
        tickets_text = "\n\n".join([
            f"ID: {ticket['id']}\nProblem: {ticket['problem']}\nSolution: {ticket['solution']}"
            for ticket in tickets
        ])
        
        prompt = f"""Customer Problem: {customer_problem}

Available Tickets:
{tickets_text}

Which ticket IDs are relevant to solving this customer's problem?"""
        
        # Clean async call - no event loop creation!
        relevance_result = await Runner.run(relevance_agent, input=prompt)
        result_text = relevance_result.final_output
        
        # Ensure we always return valid JSON
        try:
            # Try to parse the result as JSON
            parsed_result = json.loads(result_text)
            
            # Validate the structure
            if isinstance(parsed_result, dict) and "relevant_ids" in parsed_result:
                # Ensure relevant_ids is a list
                if not isinstance(parsed_result["relevant_ids"], list):
                    parsed_result["relevant_ids"] = []
                
                # Add reasoning if missing
                if "reasoning" not in parsed_result:
                    if not parsed_result["relevant_ids"]:
                        parsed_result["reasoning"] = "No tickets are relevant to this customer's problem"
                    else:
                        parsed_result["reasoning"] = f"Found {len(parsed_result['relevant_ids'])} relevant tickets"
                
                return json.dumps(parsed_result)
            else:
                # Invalid structure, return empty result
                return json.dumps({
                    "relevant_ids": [], 
                    "reasoning": "Could not determine relevant tickets - invalid response format"
                })
                
        except json.JSONDecodeError:
            # If result is not valid JSON, try to extract ticket IDs manually
            relevant_ids = []
            for ticket in tickets:
                if ticket['id'] in result_text:
                    relevant_ids.append(ticket['id'])
            
            return json.dumps({
                "relevant_ids": relevant_ids,
                "reasoning": "Extracted IDs from text response" if relevant_ids else "No relevant tickets found"
            })
        
    except Exception as e:
        print(f"Error filtering tickets: {e}")
        return json.dumps({"relevant_ids": [], "reasoning": f"Error during filtering: {str(e)}"})


@function_tool
def generate_ticket_id() -> str:
    """Generate a unique ticket ID."""
    return f"AUTO-{str(uuid.uuid4())[:8].upper()}"


class TicketAgent:
    """AI agent for customer support ticket resolution."""
    
    def __init__(self):
        """Initialize the ticket agent."""
        self.agent = Agent(
            name="Customer Support Agent",
            instructions="""You are a professional customer support agent. Your job is to resolve customer problems using the knowledge base.

Process:
1. Use get_all_tickets to get all available tickets
2. Use filter_relevant_tickets to find which tickets are relevant to the customer's problem
3. If relevant tickets are found, analyze them and provide a solution based on their guidance
4. If NO relevant tickets are found (relevant_ids array is empty), do NOT retry the tools - instead provide general helpful guidance

IMPORTANT - Avoid loops:
- Only call get_all_tickets ONCE per customer problem
- Only call filter_relevant_tickets ONCE per customer problem  
- If filter_relevant_tickets returns empty relevant_ids, accept this result and provide general guidance
- Do NOT retry the same tools multiple times

Guidelines:
- Be professional and empathetic
- Use relevant ticket solutions as guidance but personalize for the specific customer
- When no relevant tickets exist, acknowledge this and provide the best general guidance you can
- Keep solutions clear and actionable
- Always provide a direct solution, not meta-discussion about the process""",
            tools=[get_all_tickets, filter_relevant_tickets, generate_ticket_id],
        )
    
    async def generate_solution(self, problem: str) -> str:
        """Generate solution for customer problem."""
        try:
            result = await Runner.run(
                self.agent, 
                input=f"Customer problem: {problem}\n\nPlease resolve this issue."
            )
            return result.final_output
        except Exception as e:
            print(f"Error generating solution: {e}")
            return "Sorry, I'm unable to generate a solution at this time. Please contact support."
    
    async def create_ticket_with_solution(self, problem: str) -> Ticket:
        """Create a ticket with generated solution."""
        solution = await self.generate_solution(problem)
        ticket_id = f"AUTO-{str(uuid.uuid4())[:8].upper()}"
        
        return {
            "id": ticket_id,
            "problem": problem,
            "solution": solution
        }


def create_openai_service() -> OpenAIService:
    """Create OpenAI service instance."""
    return OpenAIService()


def create_ticket_agent() -> TicketAgent:
    """Create ticket agent instance."""
    return TicketAgent()


# Public API
openai_api = {
    "OpenAIService": OpenAIService,
    "TicketAgent": TicketAgent,
    "create_openai_service": create_openai_service,
    "create_ticket_agent": create_ticket_agent,
} 