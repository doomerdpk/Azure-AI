from dotenv import load_dotenv, find_dotenv
import os, asyncio
from agent_framework import Agent, AgentResponseUpdate
from agent_framework.orchestrations import HandoffBuilder
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

client = FoundryChatClient(
    project_endpoint=os.environ["AIPROJECT_ENDPOINT"],
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    credential=AzureCliCredential(),
)

triage = Agent(
    client=client, name="Triage",
    description="Routes REST API questions to the right specialist.",
    instructions="Decide if the user's question is a conceptual REST API question or a debugging/troubleshooting question, then hand off to ConceptExplainer or DebugHelper accordingly. Do not answer the question yourself.",
    default_options={"max_tokens": 500},
    require_per_service_call_history_persistence=True,
)
concept_explainer = Agent(
    client=client, name="ConceptExplainer",
    description="Explains REST API concepts.",
    instructions="Answer conceptual questions about REST APIs clearly and concisely.",
    default_options={"max_tokens": 800},
    require_per_service_call_history_persistence=True,
)
debug_helper = Agent(
    client=client, name="DebugHelper",
    description="Helps debug REST API issues.",
    instructions="Help debug the user's REST API problem with concrete, numbered troubleshooting steps.",
    default_options={"max_tokens": 1200},
    require_per_service_call_history_persistence=True,
)

workflow = (
    HandoffBuilder(participants=[triage, concept_explainer, debug_helper])
    .with_start_agent(triage)
    .add_handoff(triage, [concept_explainer, debug_helper])
    .build()
)

async def main():
    task = "My GET request to /users/123 keeps returning a 404 even though the user exists. What should I check?"
    last_author = None
    async for event in workflow.run(task, stream=True):
        if event.type in ("intermediate", "output") and isinstance(event.data, AgentResponseUpdate):
            update = event.data
            author = update.author_name
            if author != last_author:
                print(f"\n[{author}]:", end=" ")
                last_author = author
            print(update.text, end="", flush=True)
    print("\n\nWorkflow completed.")

asyncio.run(main())