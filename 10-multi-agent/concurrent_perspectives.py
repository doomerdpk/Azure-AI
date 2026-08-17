from dotenv import load_dotenv, find_dotenv
import os, asyncio
from agent_framework import Agent, AgentResponse
from agent_framework.orchestrations import ConcurrentBuilder
from agent_framework_foundry import FoundryChatClient
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

client = FoundryChatClient(
    project_endpoint=os.environ["AIPROJECT_ENDPOINT"],
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    credential=AzureCliCredential(),
)

beginner_explainer = Agent(
    client=client, name="BeginnerExplainer",
    description="Explains REST APIs to a total beginner.",
    instructions="In 2-3 sentences, explain what a REST API is for someone who has never coded before.",
    default_options={"max_tokens": 800},
)
security_reviewer = Agent(
    client=client, name="SecurityReviewer",
    description="Flags security considerations for REST APIs.",
    instructions="In 2-3 sentences, list the top security considerations someone should know before exposing a REST API.",
    default_options={"max_tokens": 800},
)
performance_reviewer = Agent(
    client=client, name="PerformanceReviewer",
    description="Flags performance considerations for REST APIs.",
    instructions="In 2-3 sentences, list the top performance considerations for designing a REST API.",
    default_options={"max_tokens": 800},
)

workflow = ConcurrentBuilder(
    participants=[beginner_explainer, security_reviewer, performance_reviewer]
).build()

async def main():
    events = await workflow.run("REST APIs")
    outputs = events.get_outputs()
    if outputs:
        final: AgentResponse = outputs[0]
        print("===== Final Aggregated Results =====")
        for msg in final.messages:
            name = msg.author_name or "assistant"
            print(f"\n[{name}]:\n{msg.text}")

asyncio.run(main())