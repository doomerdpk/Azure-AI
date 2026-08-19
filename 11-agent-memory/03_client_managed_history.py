"""
Step 13, continued — client-managed history via InMemoryHistoryProvider,
as the contrast case to script 02's service-managed (Responses API) session.

Corrected for agent-framework 1.14.0: agent_framework.azure.AzureOpenAIChatClient
no longer exists. Azure OpenAI now routes through agent_framework.openai.OpenAIChatClient
with explicit azure_endpoint/api_version (gotcha #8).

Usage (separate process invocations):
    python 03_client_managed_history.py "My name is Deepak"
    python 03_client_managed_history.py "What's my name?"
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from agent_framework import Agent, AgentSession, InMemoryHistoryProvider
from agent_framework.openai import OpenAIChatCompletionClient

SESSION_FILE = Path(__file__).parent / "client_managed_session.json"
HISTORY_SOURCE_ID = "chat_history"


def _load_session() -> AgentSession | None:
    if SESSION_FILE.exists():
        return AgentSession.from_dict(json.loads(SESSION_FILE.read_text()))
    return None


def _save_session(session: AgentSession) -> None:
    SESSION_FILE.write_text(json.dumps(session.to_dict(), indent=2))


async def main():
    client = OpenAIChatCompletionClient(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version="2025-04-01-preview",
)

    agent = Agent(
        client=client,
        name="MemoryAgent",
        instructions="You are a friendly assistant. Keep answers brief.",
        context_providers=[InMemoryHistoryProvider(HISTORY_SOURCE_ID, load_messages=True)],
        default_options={"max_tokens": 800},
    )

    session = _load_session() or agent.create_session()

    message = sys.argv[1] if len(sys.argv) > 1 else "Hello!"
    result = await agent.run(message, session=session)
    print(f"Agent: {result}")

    _save_session(session)
    d = session.to_dict()
    if d.get("service_session_id"):
        print(f"\n[unexpected: service-managed, id: {d['service_session_id']}]")
    else:
        state = d.get("state", {})
        print(f"\n[client-managed — state keys: {list(state.keys())}]")
        if HISTORY_SOURCE_ID in state:
            msgs = state[HISTORY_SOURCE_ID].get("messages", [])
            print(f"[{len(msgs)} message(s) actually stored locally]")


if __name__ == "__main__":
    asyncio.run(main())