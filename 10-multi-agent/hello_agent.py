from dotenv import load_dotenv, find_dotenv
import os, asyncio
from agent_framework import Agent
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

async def main():
    client = FoundryChatClient(
        project_endpoint=os.environ["AIPROJECT_ENDPOINT"],
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"], 
        credential=AzureCliCredential(),
    )
    agent = Agent(client=client, name="HelloAgent", instructions="You are a concise assistant.")
    result = await agent.run("Say hello and name one thing you can help with.")
    print(result)

asyncio.run(main())