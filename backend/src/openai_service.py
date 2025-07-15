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


# Global Weaviate client for function tools
_weaviate_client: Optional[weaviate.WeaviateClient] = None


def _get_weaviate_client() -> Optional[weaviate.WeaviateClient]:
    """Get or create Weaviate client."""
    global _weaviate_client
    
    if _weaviate_client is None:
        config = get_weaviate_config()
        if not config:
            print("Weaviate configuration not found")
            return None
            
        try:
            _weaviate_client = weaviate.connect_to_weaviate_cloud(
                cluster_url=config["url"],
                auth_credentials=Auth.api_key(config["api_key"]),
            )
            
            if not _weaviate_client.is_ready():
                print("Weaviate client not ready")
                return None
                
        except Exception as e:
            print(f"Error connecting to Weaviate: {e}")
            return None
    
    return _weaviate_client


# Relevance Evaluator Agent
relevance_evaluator = Agent(
    name="Relevance Evaluator",
    instructions="""You are a ticket relevance evaluator. Your job is to determine which tickets from a knowledge base are actually relevant to a customer's specific problem.

Given a customer problem and a list of potential tickets, evaluate each ticket and return only those that are truly relevant.

Be strict in your evaluation:
- Only include tickets that would genuinely help solve the customer's problem
- Exclude tickets that are only tangentially related or about different issues
- Consider the core problem, not just keyword matches

Return a JSON response with this exact format:
{
    "relevant_tickets": [
        {
            "id": "ticket_id",
            "problem": "ticket problem text", 
            "solution": "ticket solution text",
            "relevance_reason": "brief explanation why this ticket is relevant"
        }
    ],
    "total_relevant": number_of_relevant_tickets
}""",
    tools=[],
)


@function_tool
def get_relevant_tickets(customer_problem: str, limit: int = 3) -> str:
    """Search for tickets and filter for relevance to customer problem.
    
    Args:
        customer_problem: The customer's problem description
        limit: Maximum number of relevant tickets to return
        
    Returns:
        JSON string containing only relevant tickets
    """
    client = _get_weaviate_client()
    if not client:
        return json.dumps({"relevant_tickets": [], "total_relevant": 0, "error": "Unable to connect to knowledge base"})
    
    try:
        # Search for similar tickets in Weaviate
        collection = client.collections.get("Tickets")
        response = collection.query.fetch_objects(limit=10)
        
        if not response.objects:
            return json.dumps({"relevant_tickets": [], "total_relevant": 0, "error": "No tickets found in knowledge base"})
        
        # Calculate similarity scores
        problem_lower = customer_problem.lower()
        candidate_tickets = []
        
        for obj in response.objects:
            ticket_problem = str(obj.properties.get("problem", "")).lower()
            ticket_solution = str(obj.properties.get("solution", ""))
            issue_id = str(obj.properties.get("issue_id", ""))
            
            # Basic similarity scoring
            similarity_score = 0
            problem_words = problem_lower.split()
            
            for word in problem_words:
                if len(word) > 3:
                    if word in ticket_problem:
                        similarity_score += 2
                    if word in ticket_solution:
                        similarity_score += 1
            
            if similarity_score > 0:
                candidate_tickets.append({
                    "id": issue_id,
                    "problem": str(obj.properties.get("problem", "")),
                    "solution": ticket_solution,
                    "similarity_score": similarity_score
                })
        
        if not candidate_tickets:
            return json.dumps({"relevant_tickets": [], "total_relevant": 0, "message": "No similar tickets found"})
        
        # Sort by similarity and take top candidates
        candidate_tickets.sort(key=lambda x: x["similarity_score"], reverse=True)
        top_candidates = candidate_tickets[:limit * 2]  # Get more candidates for relevance evaluation
        
        # Prepare tickets for relevance evaluation
        tickets_for_evaluation = json.dumps([
            {
                "id": ticket["id"],
                "problem": ticket["problem"],
                "solution": ticket["solution"]
            }
            for ticket in top_candidates
        ], indent=2)
        
        # Use relevance evaluator to filter tickets
        async def evaluate_relevance():
            evaluation_prompt = f"""Customer Problem: {customer_problem}

Candidate Tickets:
{tickets_for_evaluation}

Please evaluate which tickets are actually relevant to this customer's problem and return the result in the specified JSON format."""
            
            result = await Runner.run(relevance_evaluator, input=evaluation_prompt)
            return result.final_output
        
        # Run relevance evaluation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            relevance_result = loop.run_until_complete(evaluate_relevance())
            return relevance_result
        finally:
            loop.close()
            
    except Exception as e:
        return json.dumps({"relevant_tickets": [], "total_relevant": 0, "error": f"Error searching tickets: {str(e)}"})


@function_tool
def create_ticket_id() -> str:
    """Generate a unique ticket ID.
    
    Returns:
        A unique ticket ID string
    """
    return f"AUTO-{str(uuid.uuid4())[:8].upper()}"


class TicketAgent:
    """AI agent for customer support ticket resolution."""
    
    def __init__(self):
        """Initialize the ticket agent."""
        self.agent = Agent(
            name="Customer Support Agent",
            instructions="""You are a professional customer support AI agent. Your job is to help resolve customer problems by:

1. Using the get_relevant_tickets function to find relevant historical tickets
2. Analyzing the solutions from relevant tickets
3. Providing a helpful, personalized solution for the customer

Guidelines:
- Always search for relevant tickets first using get_relevant_tickets
- Use the solutions from relevant tickets as guidance
- Personalize your response to the customer's specific situation  
- Be professional, empathetic, and clear
- If no relevant tickets are found, provide general helpful guidance
- Keep solutions concise but complete

Your response should be a direct solution to the customer's problem, not a meta-discussion about the process.""",
            tools=[get_relevant_tickets, create_ticket_id],
        )
    
    async def generate_solution(self, problem: str) -> str:
        """Generate a solution for a customer problem.
        
        Args:
            problem: The customer's problem description
            
        Returns:
            A solution generated by the AI agent
        """
        try:
            result = await Runner.run(
                self.agent, 
                input=f"A customer has this problem: {problem}\n\nPlease help resolve this issue."
            )
            return result.final_output
        except Exception as e:
            print(f"Error generating solution: {e}")
            return "Sorry, I'm unable to generate a solution at this time. Please contact support."
    
    async def create_ticket_with_solution(self, problem: str) -> Ticket:
        """Create a new ticket and automatically generate a solution.
        
        Args:
            problem: The customer's problem description
            
        Returns:
            A Ticket object with id, problem, and solution
        """
        # Generate solution
        solution = await self.generate_solution(problem)
        
        # Generate ticket ID
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