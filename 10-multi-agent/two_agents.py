from dotenv import load_dotenv, find_dotenv
import os, asyncio
from agent_framework import Agent
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

def make_client():
    return FoundryChatClient(
        project_endpoint=os.environ["AIPROJECT_ENDPOINT"],
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        credential=AzureCliCredential(),
    )

async def main():
    writer = Agent(
        client=make_client(),
        name="Writer",
        instructions="You write a single concise paragraph on the given topic.",
    )
    critic = Agent(
        client=make_client(),
        name="Critic",
        instructions="You critique a paragraph in 1-2 sentences: point out one weakness and one suggestion.",
    )

    draft = await writer.run("Write a paragraph explaining what a REST API is, for a beginner.")
    print("DRAFT:\n", draft, "\n")

    feedback = await critic.run(f"Critique this paragraph:\n{draft}")
    print("FEEDBACK:\n", feedback, "\n")

    revised = await writer.run(f"Revise this paragraph based on the feedback.\nParagraph: {draft}\nFeedback: {feedback}")
    print("REVISED:\n", revised)

asyncio.run(main())