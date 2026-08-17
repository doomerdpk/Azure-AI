from dotenv import load_dotenv, find_dotenv
import os, asyncio
from agent_framework import Agent, AgentResponseUpdate
from agent_framework.orchestrations import MagenticBuilder
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

client = FoundryChatClient(
    project_endpoint=os.environ["AIPROJECT_ENDPOINT"],
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    credential=AzureCliCredential(),
)

researcher = Agent(
    client=client, name="Researcher",
    description="Gathers factual points on a topic.",
    instructions="Given a topic, list 3-4 concrete factual points relevant to it. Be concise, no fluff.",
    default_options={"max_tokens": 1200},
)
writer = Agent(
    client=client, name="Writer",
    description="Writes a final recommendation from research points.",
    instructions="Given research points, write a short beginner-friendly recommendation paragraph.",
    default_options={"max_tokens": 1200},
)
manager_agent = Agent(
    client=client, name="MagenticManager",
    description="Orchestrator that coordinates the workflow.",
    instructions="You coordinate a team to complete tasks efficiently. Plan, delegate, assess progress, and finish once the task is genuinely done.",
    default_options={"max_tokens": 1200},
)

workflow = MagenticBuilder(
    participants=[researcher, writer],
    manager_agent=manager_agent,
    max_round_count=10,
    max_stall_count=3,
    max_reset_count=2,
    intermediate_output_from="all",
).build()

async def main():
    task = "Research the tradeoffs between REST and GraphQL APIs, then write a short recommendation for a beginner starting their first project."
    last_author = None
    async for event in workflow.run(task, stream=True):
        if event.type == "intermediate" and isinstance(event.data, AgentResponseUpdate):
            update = event.data
            author = update.author_name
            if author != last_author:
                print(f"\n[{author}]:", end=" ")
                last_author = author
            print(update.text, end="", flush=True)
        elif event.type == "output":
            print("\n\n===== Final Answer (Manager's synthesis) =====")
            final = event.data
            if hasattr(final, "messages"):
                for msg in final.messages:
                    print(msg.text)
            else:
                print(final)
        else:
            last_author = None
            print(f"\n[RAW EVENT type={event.type}]: {getattr(event, 'data', event)}")
    print("\n\nWorkflow completed.")

asyncio.run(main())