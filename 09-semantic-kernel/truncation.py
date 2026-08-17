import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.history_reducer.chat_history_truncation_reducer import ChatHistoryTruncationReducer

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

    # target_count: how many messages to keep after reduction
    # threshold_count: how many messages *beyond* target_count trigger a reduction
    #   (a small buffer so reduction doesn't fire on every single new message)
    history = ChatHistoryTruncationReducer(target_count=4, threshold_count=2)

    # Simulate a longer conversation — 5 fake exchanges (10 messages total)
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

        # reduce() checks whether threshold is exceeded and trims if so;
        # returns True if it actually reduced, False/None if not yet needed
        reduced = await history.reduce()
        if reduced:
            print(f"  -> Reduced! New length: {len(history.messages)}")

    print("\n--- Final history contents ---")
    for msg in history.messages:
        print(f"[{msg.role}] {msg.content}")

    # Now actually ask a real question using the (possibly truncated) history,
    # to confirm the reduced history still works fine as real conversation context
    history.add_user_message("which of the countries I asked about has the biggest population?")
    settings = AzureChatPromptExecutionSettings(
        service_id="aoai-learning-01",
        max_completion_tokens=600,
    )
    response = await chat_service.get_chat_message_content(chat_history=history, settings=settings)
    print("\nFinal live response:", response)


if __name__ == "__main__":
    asyncio.run(main())