import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.contents.history_reducer.chat_history_summarization_reducer import ChatHistorySummarizationReducer

AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_KEY"]
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


async def main() -> None:
    chat_service = AzureChatCompletion(
        service_id="aoai-learning-01",
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-10-21",
    )

    history = ChatHistorySummarizationReducer(
        service=chat_service,           # the LLM that will generate the summary
        target_count=4,                 # keep 4 messages (or summary + recent messages) after reduction
        threshold_count=2,              # same buffer logic as truncation
        execution_settings=AzureChatPromptExecutionSettings(
            service_id="aoai-learning-01",
            max_completion_tokens=600,  # summarization is its own LLM call — needs its own reasoning-token budget
        ),
    )

    fake_turns = [
        ("What's the capital of France?", "Paris."),
        ("What's the capital of Japan?", "Tokyo."),
        ("What's the capital of Italy?", "Rome."),
        ("What's the capital of Germany?", "Berlin."),
        ("What's the capital of Spain?", "Madrid."),
    ]

    for user_msg, assistant_msg in fake_turns:
        history.add_user_message(user_msg)
        history.add_assistant_message(assistant_msg)
        print(f"After adding turn, history length: {len(history.messages)}")

        reduced = await history.reduce()
        if reduced:
            print(f"  -> Reduced! New length: {len(history.messages)}")

    print("\n--- Final history contents ---")
    for msg in history.messages:
        print(f"[{msg.role}] {msg.content}")

    history.add_user_message("which of the countries I asked about has the biggest population?")
    settings = AzureChatPromptExecutionSettings(
        service_id="aoai-learning-01",
        max_completion_tokens=600,
    )
    response = await chat_service.get_chat_message_content(chat_history=history, settings=settings)
    print("\nFinal live response:", response)


if __name__ == "__main__":
    asyncio.run(main())