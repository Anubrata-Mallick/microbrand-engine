import os
import asyncio
from typing import List, Dict, Any, Optional
from backboard import BackboardClient
from dotenv import load_dotenv

load_dotenv()

class FrameworkBrandMemory:
    """Manages brand memory using Backboard's persistent memory layer."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("BACKBOARD_API_KEY")
        if not self.api_key:
            raise ValueError("BACKBOARD_API_KEY is not set in environment or .env file.")
        self.client = BackboardClient(api_key=self.api_key)

    async def initialize_assistant(self, brand_name: str) -> str:
        """Creates or registers an assistant representing the brand workspace."""
        assistant = await self.client.create_assistant(
            name=f"{brand_name} Voice Engine",
            system_prompt=(
                f"You are the brand guardian and copywriter for {brand_name}. "
                "Enforce strict brand tone, guidelines, and forbidden vocabulary."
            )
        )
        return str(assistant.assistant_id)
    
    async def save_brand_rule(self, assistant_id: str, rule: str, category: str = "tone"):
        """Saves a brand guideline or persona trait into semantic memory."""
        await self.client.add_memory(
            assistant_id=assistant_id,
            content=rule,
            metadata={"category": category}
        )

    async def get_brand_context(self, assistant_id: str) -> List[str]:
        """Retrieves active brand memories to inject into the LangGraph state."""
        memories_response = await self.client.get_memories(
            assistant_id=assistant_id, 
            page=1, 
            page_size=25
        )
        return [mem.content for mem in memories_response.memories]