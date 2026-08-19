"""
Step 13, continued — full session serialization (chat history + state),
using the framework's built-in AgentSession.to_dict() / from_dict()
instead of hand-rolled fact extraction.

Usage (separate process invocations):
    python 02_session_serialization.py "My name is Deepak"
    python 02_session_serialization.py "What's my name?"
    python 02_session_serialization.py "What did I ask you first?"
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from agent_framework import Agent, AgentSession
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

SESSION_FILE = Path(__file__).parent / "session_state.json"


def _load_session() -> AgentSession | None:
    if SESSION_FILE.exists():
        return AgentSession.from_dict(json.loads(SESSION_FILE.read_text()))
    return None


def _save_session(session: AgentSession) -> None:
    SESSION_FILE.write_text(json.dumps(session.to_dict(), indent=2))


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
        default_options={"max_tokens": 800},
    )

    session = _load_session() or agent.create_session()

    message = sys.argv[1] if len(sys.argv) > 1 else "Hello!"
    result = await agent.run(message, session=session)
    print(f"Agent: {result}")

    _save_session(session)
    d = session.to_dict()
    if d.get("service_session_id"):
        print(f"\n[session saved — service-managed, conversation id: {d['service_session_id']}]")
    else:
        print(f"\n[session saved — client-managed, state keys: {list(d.get('state', {}).keys())}]")


if __name__ == "__main__":
    asyncio.run(main())