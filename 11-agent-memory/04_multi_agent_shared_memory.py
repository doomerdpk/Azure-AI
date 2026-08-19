"""
Step 13, continued — shared memory across a MULTI-AGENT session (v2).

Corrected design after introspecting agent_framework 1.14.0 directly
(gotcha #1 in full effect -- five rounds of signature drift from docs).

Real mechanism, confirmed via agent_framework._agents source:
    - Agent does NOT take a history_provider= kwarg. It takes
      context_providers=[...] (plural, list of ContextProvider).
    - If you pass session=<AgentSession> to .run() and configure NO
      context_providers, the framework auto-injects a default
      InMemoryHistoryProvider (DEFAULT_SOURCE_ID) that stores messages
      under session.state[source_id].
    - Two agents sharing the SAME AgentSession object therefore share
      the SAME state slot -- that's the actual cross-agent memory
      mechanism, no manual provider wiring needed for the baseline case.
    - AgentSession.to_dict()/from_dict() (already used in script 02)
      serializes session.state, so it round-trips the shared history
      across process invocations too.

Dropped HandoffBuilder from this version: it added two more layers of
unverified API surface (agent_framework.orchestrations, gotcha #9) that
aren't needed to answer the core question. Once this baseline is proven,
wiring HandoffBuilder on top is a natural follow-up, not a prerequisite.

Usage (separate process invocations):
    python 04_multi_agent_shared_memory.py triage "My name is Deepak"
    python 04_multi_agent_shared_memory.py specialist "What's my name?"
    python 04_multi_agent_shared_memory.py specialist "What did I first tell the triage agent?"
"""

import sys
import json
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

from agent_framework.openai import OpenAIChatCompletionClient
from agent_framework import Agent, AgentSession

SESSION_FILE = Path(__file__).parent / ".shared_memory_session.json"
SESSION_ID = "triage-specialist-shared"


def load_session() -> AgentSession:
    if SESSION_FILE.exists():
        data = json.loads(SESSION_FILE.read_text())
        return AgentSession.from_dict(data)
    return AgentSession(session_id=SESSION_ID)


def save_session(session: AgentSession) -> None:
    SESSION_FILE.write_text(json.dumps(session.to_dict(), indent=2, default=str))


def build_chat_client() -> OpenAIChatCompletionClient:
    return OpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_KEY"],
        api_version="2025-04-01-preview",
    )


def build_agents():
    chat_client = build_chat_client()

    # client and instructions are positional (confirmed via Agent.__init__
    # signature) -- NOT chat_client= / history_provider= kwargs, which is
    # what our earlier version wrongly assumed.
    triage_agent = Agent(
        chat_client,
        "You are a general intake agent. Answer briefly. If the user "
        "asks something deeply technical, mention you'd hand off to a "
        "specialist, but for this script just answer directly.",
        name="triage_agent",
        default_options={"max_tokens": 800},  # gotcha #2
    )

    specialist_agent = Agent(
        chat_client,
        "You are a specialist follow-up agent. You share conversation "
        "history with the triage agent -- use it to recall anything "
        "the user told the triage agent earlier, even though you are "
        "a different agent instance.",
        name="specialist_agent",
        default_options={"max_tokens": 800},
    )

    return triage_agent, specialist_agent


async def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return

    which_agent, message = sys.argv[1], sys.argv[2]
    if which_agent not in ("triage", "specialist"):
        print("First arg must be 'triage' or 'specialist'")
        return

    session = load_session()
    triage_agent, specialist_agent = build_agents()
    agent = triage_agent if which_agent == "triage" else specialist_agent

    print(f"--- talking to {agent.name} ---")
    response = await agent.run(message, session=session)
    print(response.text if hasattr(response, "text") else response)

    save_session(session)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())