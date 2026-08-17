from dotenv import load_dotenv, find_dotenv
import os, asyncio
from agent_framework import Agent, AgentResponseUpdate
from agent_framework.orchestrations import GroupChatBuilder
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

client = FoundryChatClient(
    project_endpoint=os.environ["AIPROJECT_ENDPOINT"],
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    credential=AzureCliCredential(),
)

writer = Agent(
    client=client, name="Writer",
    description="Writes a paragraph, then revises based on feedback.",
    instructions="Write a concise paragraph on the given topic. If feedback appears in the conversation, revise accordingly.",
)
critic = Agent(
    client=client, name="Critic",
    description="Critiques the Writer's paragraph.",
    instructions="Critique the most recent paragraph in 1-2 sentences: one weakness, one suggestion. If the paragraph is already strong, say 'Looks good, no further changes needed.'",
)

orchestrator_agent = Agent(
    name="Orchestrator",
    description="Coordinates the Writer/Critic conversation.",
    instructions="""
You coordinate a two-agent conversation to produce a good beginner-friendly paragraph.

Guidelines:
- Start with Writer to produce a first draft.
- Then have Critic review it.
- If Critic found a real weakness, send it back to Writer to revise once more.
- If Critic says the paragraph looks good, stop immediately — do not loop further.
""",
    client=client,
)

workflow = GroupChatBuilder(
    participants=[writer, critic],
    termination_condition=lambda conversation: sum(1 for m in conversation if m.role == "assistant") >= 6,  # hard safety cap
    orchestrator_agent=orchestrator_agent,
    intermediate_output_from=[writer, critic],
).build()

async def main():
    task = "Write a paragraph explaining what a REST API is, for a beginner."
    last_author = None
    stream = workflow.run(task, stream=True)
    async for event in stream:
        if event.type in ("intermediate", "output") and isinstance(event.data, AgentResponseUpdate):
            author = event.data.author_name
            if author != last_author:
                print(f"\n[{author}]:", end=" ")
                last_author = author
            print(event.data.text, end="", flush=True)
    print("\n\nWorkflow completed.")

asyncio.run(main())