"""
Step 13 sanity check — agent memory across separate process invocations.

Usage (three separate runs, proving persistence survives process exit):
    python 01_single_agent_memory.py
    python 01_single_agent_memory.py "My name is Deepak"
    python 01_single_agent_memory.py "What's 2 + 2?"
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from agent_framework import Agent, ContextProvider
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

MEMORY_FILE = Path(__file__).parent / "memory_state.json"


def _load_state() -> dict[str, Any]:
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {}


def _save_state(state: dict[str, Any]) -> None:
    MEMORY_FILE.write_text(json.dumps(state, indent=2))


class DiskUserMemoryProvider(ContextProvider):
    """Persists user_name to a JSON file so it survives separate process
    invocations — not just separate calls within one run's session object."""

    DEFAULT_SOURCE_ID = "user_memory"

    def __init__(self):
        super().__init__(self.DEFAULT_SOURCE_ID)

    async def before_run(self, *, agent, session, context, state):
        user_name = _load_state().get("user_name")
        if user_name:
            context.extend_instructions(
                self.source_id,
                f"The user's name is {user_name}. Always address them by name.",
            )
        else:
            context.extend_instructions(
                self.source_id,
                "You don't know the user's name yet. Ask for it politely.",
            )

    async def after_run(self, *, agent, session, context, state):
        disk_state = _load_state()
        for msg in context.input_messages:
            text = msg.text if hasattr(msg, "text") else ""
            if isinstance(text, str) and "my name is" in text.lower():
                disk_state["user_name"] = (
                    text.lower().split("my name is")[-1].strip().split()[0].capitalize()
                )
                _save_state(disk_state)
                break


async def main():
    client = FoundryChatClient(
        project_endpoint=os.environ["AIPROJECT_ENDPOINT"],
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="MemoryAgent",
        instructions="You are a friendly assistant. Keep answers brief.",
        context_providers=[DiskUserMemoryProvider()],
        default_options={"max_tokens": 800}, 
    )

    session = agent.create_session()
    message = sys.argv[1] if len(sys.argv) > 1 else "Hello! What's the square root of 9?"
    result = await agent.run(message, session=session)

    print(f"Agent: {result}")
    print(f"\n[disk state] {_load_state()}")


if __name__ == "__main__":
    asyncio.run(main())