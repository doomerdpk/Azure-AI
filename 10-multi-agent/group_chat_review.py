from dotenv import load_dotenv, find_dotenv
import os, asyncio
from agent_framework import Agent, AgentResponseUpdate
from agent_framework.orchestrations import GroupChatBuilder, GroupChatState
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
# critic = Agent(
#     client=client, name="Critic",
#     description="Critiques the Writer's paragraph.",
#     instructions="Critique the most recent paragraph in 1-2 sentences: one weakness, one suggestion.",
# )

critic = Agent(
    client=client, name="Critic",
    description="Critiques the Writer's paragraph.",
    instructions=(
        "Critique the most recent paragraph only if a genuine beginner would be confused by it. "
        "If so, give exactly one weakness and one suggestion, in 1-2 sentences. "
        "Do not ask for further simplification once jargon has already been explained with an example. "
        "If the paragraph is clear enough for a beginner, respond with exactly: 'Looks good, no further changes needed.'"
    ),
)

def round_robin_selector(state: GroupChatState) -> str:
    participant_names = list(state.participants.keys())
    return participant_names[state.current_round % len(participant_names)]

workflow = GroupChatBuilder(
    participants=[writer, critic],
    termination_condition=lambda conversation: len(conversation) >= 4,  # Writer, Critic, Writer, done
    selection_func=round_robin_selector,
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