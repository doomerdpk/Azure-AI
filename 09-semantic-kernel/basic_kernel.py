import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings

load_dotenv(find_dotenv())

AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_KEY"]
AZURE_OPENAI_DEPLOYMENT = os.environ.get(
    "AZURE_OPENAI_CHAT_DEPLOYMENT",
    os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-5-mini"),
)


async def main() -> None:
    kernel = Kernel()

    chat_service = AzureChatCompletion(
        service_id="aoai-learning-01",
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-10-21", 
    )
    kernel.add_service(chat_service)

    history = ChatHistory()
    history.add_user_message("In one sentence, what is Semantic Kernel?")

    settings = AzureChatPromptExecutionSettings()

    response = await chat_service.get_chat_message_content(
        chat_history=history,
        settings=settings,
    )

    print("SK -> Azure OpenAI response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())