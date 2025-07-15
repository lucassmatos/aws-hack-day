"""OpenAI service for AI operations."""

import os
import json
import uuid
import asyncio
import logging
from typing import Optional, Dict, Any, List, TypedDict
from openai import OpenAI
import weaviate
from weaviate.classes.init import Auth
from config import get_openai_config, get_weaviate_config

# OpenAI agents imports
from agents import Agent, Runner, function_tool
from .dynamodb_client import save_ticket, create_table_if_not_exists

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import types
from .ticket_types import Ticket


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
        logger.info("🔌 Creating new Weaviate client...")
        
        config = get_weaviate_config()
        if not config:
            logger.error("❌ No Weaviate config available")
            return None
            
        try:
            logger.info(f"🔗 Connecting to Weaviate at {config['url']}")
            
            _weaviate_client = weaviate.connect_to_weaviate_cloud(
                cluster_url=config["url"],
                auth_credentials=Auth.api_key(config["api_key"]),
            )
            
            if not _weaviate_client.is_ready():
                logger.error("❌ Weaviate client not ready")
                return None
            
            logger.info("✅ Weaviate client connected and ready")
                
        except Exception as e:
            logger.error(f"❌ Error connecting to Weaviate: {e}")
            return None
    else:
        logger.debug("♻️ Reusing existing Weaviate client")
    
    return _weaviate_client


# Relevance Evaluator Agent
relevance_agent = Agent(
    name="Relevance Evaluator",
    instructions="""You are a relevance evaluator. Given a customer problem and a list of support tickets, determine which tickets are actually relevant to solving the customer's problem.

Be strict - only return IDs of tickets that would genuinely help solve the customer's specific issue. Ignore tickets that are only tangentially related or about different problems entirely.

CRITICAL: Return ONLY a valid JSON object with this EXACT format - no additional text before or after:
{
    "relevant_ids": ["ID1", "ID2", "ID3"],
    "reasoning": "Brief explanation of your filtering decisions"
}

Do NOT include any other text, explanations, or formatting. Just the JSON object.""",
    tools=[],
)


@function_tool
async def get_all_tickets() -> str:
    """Get all tickets from the knowledge base.
    
    Returns:
        JSON string with all tickets
    """
    logger.info("🎫 get_all_tickets() called - fetching tickets from Weaviate")
    
    client = _get_weaviate_client()
    if not client:
        logger.error("❌ No Weaviate client available")
        return json.dumps([])
    
    try:
        collection = client.collections.get("Tickets")
        response = collection.query.fetch_objects(limit=10)
        
        if not response.objects:
            logger.warning("⚠️ No tickets found in Weaviate")
            return json.dumps([])
        
        # Convert to list
        all_tickets = []
        for obj in response.objects:
            all_tickets.append({
                "id": str(obj.properties.get("issue_id", "")),
                "problem": str(obj.properties.get("problem", "")),
                "solution": str(obj.properties.get("solution", ""))
            })
        
        logger.info(f"✅ Found {len(all_tickets)} tickets in Weaviate")
        logger.debug(f"Ticket IDs: {[t['id'] for t in all_tickets]}")
        
        result = json.dumps(all_tickets)
        logger.debug(f"Returning JSON with {len(result)} characters")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error getting tickets: {e}")
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
    logger.info(f"🔍 filter_relevant_tickets() called")
    logger.info(f"Customer problem: {customer_problem}")
    
    try:
        tickets = json.loads(all_tickets_json)
        logger.info(f"📋 Parsed {len(tickets)} tickets from JSON")
        
        if not tickets:
            logger.warning("⚠️ No tickets to filter")
            return json.dumps({"relevant_ids": [], "reasoning": "No tickets available"})
        
        tickets_text = "\n\n".join([
            f"ID: {ticket['id']}\nProblem: {ticket['problem']}\nSolution: {ticket['solution']}"
            for ticket in tickets
        ])
        
        prompt = f"""Customer Problem: {customer_problem}

Available Tickets:
{tickets_text}

Which ticket IDs are relevant to solving this customer's problem?"""
        
        logger.info("🤖 Calling relevance agent...")
        logger.debug(f"Prompt length: {len(prompt)} characters")
        
        # Clean async call - no event loop creation!
        relevance_result = await Runner.run(relevance_agent, input=prompt)
        result_text = relevance_result.final_output
        
        logger.info(f"🎯 Relevance agent returned: {result_text}")
        
        # Ensure we always return valid JSON
        try:
            # Try to parse the result as JSON
            parsed_result = json.loads(result_text)
            logger.info(f"✅ Successfully parsed JSON result")
            
            # Validate the structure
            if isinstance(parsed_result, dict) and "relevant_ids" in parsed_result:
                # Ensure relevant_ids is a list
                if not isinstance(parsed_result["relevant_ids"], list):
                    logger.warning("⚠️ relevant_ids was not a list, converting to empty list")
                    parsed_result["relevant_ids"] = []
                
                # Add reasoning if missing
                if "reasoning" not in parsed_result:
                    if not parsed_result["relevant_ids"]:
                        parsed_result["reasoning"] = "No tickets are relevant to this customer's problem"
                    else:
                        parsed_result["reasoning"] = f"Found {len(parsed_result['relevant_ids'])} relevant tickets"
                
                logger.info(f"🎯 Final result: {len(parsed_result['relevant_ids'])} relevant tickets: {parsed_result['relevant_ids']}")
                return json.dumps(parsed_result)
            else:
                logger.error("❌ Invalid JSON structure - missing relevant_ids")
                # Invalid structure, return empty result
                return json.dumps({
                    "relevant_ids": [], 
                    "reasoning": "Could not determine relevant tickets - invalid response format"
                })
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error: {e}")
            logger.info("🔧 Attempting manual ID extraction...")
            
            # If result is not valid JSON, try to extract ticket IDs manually
            relevant_ids = []
            for ticket in tickets:
                if ticket['id'] in result_text:
                    relevant_ids.append(ticket['id'])
            
            logger.info(f"🔧 Extracted IDs manually: {relevant_ids}")
            return json.dumps({
                "relevant_ids": relevant_ids,
                "reasoning": "Extracted IDs from text response" if relevant_ids else "No relevant tickets found"
            })
        
    except Exception as e:
        logger.error(f"❌ Error filtering tickets: {e}")
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
        logger.info(f"🤖 TicketAgent.generate_solution() called")
        logger.info(f"Problem: {problem}")
        
        try:
            logger.info("🚀 Starting Runner.run() with TicketAgent...")
            
            result = await Runner.run(
                self.agent, 
                input=f"Customer problem: {problem}\n\nPlease resolve this issue."
            )
            
            logger.info(f"✅ Runner.run() completed successfully")
            logger.info(f"Final output: {result.final_output}")
            
            return result.final_output
        except Exception as e:
            logger.error(f"❌ Error generating solution: {e}")
            logger.error(f"Exception type: {type(e).__name__}")
            return "Sorry, I'm unable to generate a solution at this time. Please contact support."
    
    async def create_ticket_with_solution(self, problem: str) -> Ticket:
        """Create a ticket with generated solution and save to DynamoDB."""
        logger.info(f"🎫 Creating new ticket for problem: {problem}")
        
        solution = await self.generate_solution(problem)
        ticket_id = f"AUTO-{str(uuid.uuid4())[:8].upper()}"
        
        # Simple category detection based on keywords
        problem_lower = problem.lower()
        category = "General Support"
        
        if any(word in problem_lower for word in ["payment", "billing", "charge", "refund", "card"]):
            category = "Payment & Billing Issues"
        elif any(word in problem_lower for word in ["book", "reservation", "cancel", "availability"]):
            category = "Booking & Reservation Issues"
        elif any(word in problem_lower for word in ["app", "login", "password", "technical", "bug", "error"]):
            category = "Technical & App Issues"
        elif any(word in problem_lower for word in ["property", "stay", "check", "room", "clean"]):
            category = "Property & Stay Issues"
        elif any(word in problem_lower for word in ["host", "seller", "owner", "listing"]):
            category = "Host/Seller Issues"
        
        from datetime import datetime
        timestamp = datetime.utcnow().isoformat()
        
        ticket: Ticket = {
            "id": ticket_id,
            "problem": problem,
            "solution": solution,
            "category": category,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        # Save to DynamoDB
        logger.info(f"💾 Saving ticket {ticket_id} to DynamoDB...")
        
        # Ensure table exists first
        if not create_table_if_not_exists():
            logger.warning("⚠️ Could not create/verify DynamoDB table")
        
        if save_ticket(ticket):
            logger.info(f"✅ Ticket {ticket_id} saved successfully")
        else:
            logger.warning(f"⚠️ Failed to save ticket {ticket_id} to DynamoDB")
        
        return ticket


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