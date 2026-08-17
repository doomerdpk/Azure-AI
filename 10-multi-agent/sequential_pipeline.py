from dotenv import load_dotenv, find_dotenv
import os, asyncio
from agent_framework import Agent, AgentResponseUpdate
from agent_framework.orchestrations import SequentialBuilder
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
    description="Writes a first draft paragraph.",
    instructions="Write a concise paragraph explaining the given topic for a beginner.",
    default_options={"max_tokens": 800},
)
critic = Agent(
    client=client, name="Critic",
    description="Critiques the Writer's paragraph.",
    instructions="Critique the paragraph in 1-2 sentences: one weakness, one suggestion. Do not rewrite it yourself.",
    default_options={"max_tokens": 800},
)
editor = Agent(
    client=client, name="Editor",
    description="Produces the final polished version.",
    instructions="You will see a draft paragraph and a critique. Produce ONE final, polished paragraph that addresses the critique. Output only the final paragraph, nothing else.",
    default_options={"max_tokens": 800},
)

workflow = SequentialBuilder(
    participants=[writer, critic, editor],
    intermediate_output_from="all",
).build()

async def main():
    task = "Write a paragraph explaining what a REST API is, for a beginner."
    last_author = None
    async for event in workflow.run(task, stream=True):
        if event.type in ("intermediate", "output") and isinstance(event.data, AgentResponseUpdate):
            update = event.data
            author = update.author_name
            if author != last_author:
                if last_author is not None:
                    print()
                print(f"\n[{author}]:", end=" ")
                last_author = author
            print(update.text, end="", flush=True)
    print("\n\nWorkflow completed.")

asyncio.run(main())