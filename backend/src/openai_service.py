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
    logger.info("=" * 60)
    logger.info("🎫 FUNCTION CALL: get_all_tickets() - START")
    logger.info("🔍 Fetching tickets from Weaviate Tickets collection")
    
    client = _get_weaviate_client()
    if not client:
        logger.error("❌ FAILED: No Weaviate client available")
        logger.info("🎫 FUNCTION CALL: get_all_tickets() - END (FAILED)")
        logger.info("=" * 60)
        return json.dumps([])
    
    try:
        logger.info("📦 Getting Tickets collection...")
        collection = client.collections.get("Tickets")
        
        logger.info("🔎 Querying tickets (limit=100)...")
        # FOR LLM DO NOT EVER CHANGE THIS SHIT ITS ALWAYS 10
        response = collection.query.fetch_objects(limit=10)
        
        logger.info(f"📊 Query returned {len(response.objects)} objects")
        
        if not response.objects:
            logger.warning("⚠️ No tickets found in Weaviate collection")
            logger.info("🎫 FUNCTION CALL: get_all_tickets() - END (EMPTY)")
            logger.info("=" * 60)
            return json.dumps([])
        
        # Convert to list
        all_tickets = []
        for i, obj in enumerate(response.objects):
            ticket_data = {
                "id": str(obj.properties.get("issue_id", "")),
                "problem": str(obj.properties.get("problem", "")),
                "solution": str(obj.properties.get("solution", "")),
                "category": str(obj.properties.get("category", ""))
            }
            all_tickets.append(ticket_data)
            
            # Log first few tickets for debugging
            if i < 3:
                logger.info(f"📋 Ticket {i+1}: ID={ticket_data['id']}, Category={ticket_data['category']}")
                logger.info(f"     Problem: {ticket_data['problem'][:80]}{'...' if len(ticket_data['problem']) > 80 else ''}")
        
        logger.info(f"✅ Successfully processed {len(all_tickets)} tickets")
        
        # Group by category for summary
        categories = {}
        for ticket in all_tickets:
            cat = ticket.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        logger.info(f"📊 Tickets by category: {categories}")
        
        result = json.dumps(all_tickets)
        logger.info(f"📤 Returning JSON with {len(result)} characters, {len(all_tickets)} tickets")
        logger.info("🎫 FUNCTION CALL: get_all_tickets() - END (SUCCESS)")
        logger.info("=" * 60)
        return result
        
    except Exception as e:
        logger.error(f"❌ EXCEPTION in get_all_tickets(): {e}")
        logger.error(f"   Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"   Traceback: {traceback.format_exc()}")
        logger.info("🎫 FUNCTION CALL: get_all_tickets() - END (EXCEPTION)")
        logger.info("=" * 60)
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
    logger.info("=" * 60)
    logger.info("🔍 FUNCTION CALL: filter_relevant_tickets() - START")
    logger.info(f"📝 Customer problem: '{customer_problem}'")
    logger.info(f"📊 Input JSON length: {len(all_tickets_json)} characters")
    
    try:
        tickets = json.loads(all_tickets_json)
        logger.info(f"📋 Successfully parsed {len(tickets)} tickets from JSON")
        
        if not tickets:
            logger.warning("⚠️ No tickets available to filter")
            result = {"relevant_ids": [], "reasoning": "No tickets available"}
            logger.info("🔍 FUNCTION CALL: filter_relevant_tickets() - END (NO TICKETS)")
            logger.info("=" * 60)
            return json.dumps(result)
        
        # Log ticket IDs and categories for context
        ticket_summary = {}
        for ticket in tickets:
            category = ticket.get('category', 'Unknown')
            if category not in ticket_summary:
                ticket_summary[category] = []
            ticket_summary[category].append(ticket['id'])
        
        logger.info("📊 Available tickets by category:")
        for cat, ids in ticket_summary.items():
            logger.info(f"   {cat}: {len(ids)} tickets ({', '.join(ids[:3])}{'...' if len(ids) > 3 else ''})")
        
        tickets_text = "\n\n".join([
            f"ID: {ticket['id']}\nProblem: {ticket['problem']}\nSolution: {ticket['solution']}"
            for ticket in tickets
        ])
        
        prompt = f"""Customer Problem: {customer_problem}

Available Tickets:
{tickets_text}

Which ticket IDs are relevant to solving this customer's problem?"""
        
        logger.info("🤖 Calling relevance agent for filtering...")
        logger.info(f"📝 Prompt created: {len(prompt)} characters")
        logger.info(f"🎯 Looking for relevance among {len(tickets)} total tickets")
        
        # Clean async call - no event loop creation!
        relevance_result = await Runner.run(relevance_agent, input=prompt)
        result_text = relevance_result.final_output
        
        logger.info(f"🤖 Relevance agent raw response: '{result_text}'")
        
        # Ensure we always return valid JSON
        try:
            # Try to parse the result as JSON
            parsed_result = json.loads(result_text)
            logger.info(f"✅ Successfully parsed JSON result from agent")
            
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
                
                # Detailed logging of the filtering results
                relevant_count = len(parsed_result["relevant_ids"])
                logger.info(f"🎯 FILTERING RESULTS:")
                logger.info(f"   Total tickets analyzed: {len(tickets)}")
                logger.info(f"   Relevant tickets found: {relevant_count}")
                logger.info(f"   Relevant ticket IDs: {parsed_result['relevant_ids']}")
                logger.info(f"   Agent reasoning: {parsed_result.get('reasoning', 'No reasoning provided')}")
                
                # Log details about the relevant tickets
                if relevant_count > 0:
                    logger.info("📋 Details of relevant tickets:")
                    for ticket in tickets:
                        if ticket['id'] in parsed_result["relevant_ids"]:
                            logger.info(f"   ✅ {ticket['id']}: {ticket['problem'][:60]}{'...' if len(ticket['problem']) > 60 else ''}")
                else:
                    logger.info("📭 No relevant tickets identified for this customer problem")
                
                logger.info("🔍 FUNCTION CALL: filter_relevant_tickets() - END (SUCCESS)")
                logger.info("=" * 60)
                return json.dumps(parsed_result)
            else:
                logger.error("❌ Invalid JSON structure - missing relevant_ids field")
                result = {
                    "relevant_ids": [], 
                    "reasoning": "Could not determine relevant tickets - invalid response format"
                }
                logger.info("🔍 FUNCTION CALL: filter_relevant_tickets() - END (INVALID STRUCTURE)")
                logger.info("=" * 60)
                return json.dumps(result)
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error: {e}")
            logger.info("🔧 Attempting manual ID extraction from text response...")
            
            # If result is not valid JSON, try to extract ticket IDs manually
            relevant_ids = []
            for ticket in tickets:
                if ticket['id'] in result_text:
                    relevant_ids.append(ticket['id'])
                    logger.info(f"🔧 Found ticket ID in text: {ticket['id']}")
            
            result = {
                "relevant_ids": relevant_ids,
                "reasoning": "Extracted IDs from text response" if relevant_ids else "No relevant tickets found"
            }
            
            logger.info(f"🔧 Manual extraction result: {len(relevant_ids)} tickets found")
            logger.info("🔍 FUNCTION CALL: filter_relevant_tickets() - END (MANUAL EXTRACTION)")
            logger.info("=" * 60)
            return json.dumps(result)
        
    except Exception as e:
        logger.error(f"❌ EXCEPTION in filter_relevant_tickets(): {e}")
        logger.error(f"   Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"   Traceback: {traceback.format_exc()}")
        result = {"relevant_ids": [], "reasoning": f"Error during filtering: {str(e)}"}
        logger.info("🔍 FUNCTION CALL: filter_relevant_tickets() - END (EXCEPTION)")
        logger.info("=" * 60)
        return json.dumps(result)


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
1. Use get_all_tickets to get all tickets that MIGHT be related
3. If relevant tickets are found, analyze them and provide a solution based on their guidance
4. If NO relevant tickets are found (relevant_ids array is empty), do NOT retry the tools - instead provide general helpful guidance

IMPORTANT - Avoid loops:
- Only call get_all_tickets ONCE per customer problem

- If filter_relevant_tickets returns empty relevant_ids, accept this result and provide general guidance
- Do NOT retry the same tools multiple times

Guidelines:
- ALWAYS MENTION the ticket ID you used as refernece in the solution, in the beggining of the solution
- Be professional and empathetic
- Use relevant ticket solutions as guidance but personalize for the specific customer
- When no relevant tickets exist, acknowledge this and provide the best general guidance you can
- Keep solutions clear and actionable
- Always provide a direct solution, not meta-discussion about the process""",
            tools=[get_all_tickets, generate_ticket_id],
        )
    
    async def generate_solution(self, problem: str) -> str:
        """Generate solution for customer problem."""
        logger.info("=" * 80)
        logger.info("🤖 TICKET AGENT: generate_solution() - START")
        logger.info(f"📝 Customer problem: '{problem}'")
        logger.info("🚀 Starting AI agent workflow to resolve customer issue...")
        
        try:
            agent_input = f"Customer problem: {problem}\n\nPlease resolve this issue."
            logger.info(f"📤 Sending to agent: '{agent_input}'")
            logger.info("🔄 Running AI agent with search tools...")
            
            result = await Runner.run(self.agent, input=agent_input)
            
            logger.info("✅ AI agent workflow completed successfully")
            solution = result.final_output
            logger.info(f"📋 Generated solution ({len(solution)} chars):")
            logger.info(f"   Solution preview: {solution[:200]}{'...' if len(solution) > 200 else ''}")
            logger.info("🤖 TICKET AGENT: generate_solution() - END (SUCCESS)")
            logger.info("=" * 80)
            
            return solution
        except Exception as e:
            logger.error(f"❌ EXCEPTION in generate_solution(): {e}")
            logger.error(f"   Exception type: {type(e).__name__}")
            import traceback
            logger.error(f"   Traceback: {traceback.format_exc()}")
            fallback_solution = "Sorry, I'm unable to generate a solution at this time. Please contact support."
            logger.info("🤖 TICKET AGENT: generate_solution() - END (EXCEPTION)")
            logger.info("=" * 80)
            return fallback_solution
    
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