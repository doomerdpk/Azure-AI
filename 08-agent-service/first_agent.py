from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import AzureCliCredential

client = AIProjectClient(
    endpoint=os.environ["AIPROJECT_ENDPOINT"],
    credential=AzureCliCredential()
)
openai_client = client.get_openai_client()

# Step 1: Create the agent (now versioned)
agent = client.agents.create_version(
    agent_name="my-first-agent",
    definition=PromptAgentDefinition(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions="You are a helpful DevOps assistant. Answer questions about Azure, CI/CD, and cloud infrastructure concisely."
    )
)
print(f"Agent created: {agent.name} (version {agent.version})")

# Step 2: Create a conversation (replaces thread)
conversation = openai_client.conversations.create()
print(f"Conversation created: {conversation.id}")

# Step 3: Get a response (replaces message + run + poll)
response = openai_client.responses.create(
    input="What are the key differences between Azure DevOps Pipelines and GitHub Actions?",
    conversation=conversation.id,
    extra_body={
        "agent_reference": {
            "name": agent.name,
            "type": "agent_reference"
        }
    }
)

# Step 4: Print response
for item in response.output:
    if item.type == "message":
        for block in item.content:
            print(f"\nAgent response:\n{block.text}")

# Cleanup
client.agents.delete(agent.name)
print("\nAgent deleted")