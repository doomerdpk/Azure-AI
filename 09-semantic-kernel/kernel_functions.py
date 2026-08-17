import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai import FunctionChoiceBehavior

AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_KEY"]
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


class TripPlugin:
    """Two functions where the second depends on the first's output —
    forces the model to chain calls rather than answer from one lookup."""

    @kernel_function(
        name="get_weather",
        description="Get the current weather for a given city.",
    )
    def get_weather(self, city: str) -> str:
        fake_data = {
            "mumbai": "32°C, humid, chance of rain",
            "delhi": "38°C, clear skies",
            "manali": "8°C, snowing",
        }
        return fake_data.get(city.lower(), f"No weather data available for {city}.")

    @kernel_function(
        name="suggest_packing_list",
        description="Given a weather description, suggest what to pack for the trip.",
    )
    def suggest_packing_list(self, weather_description: str) -> str:
        weather_description = weather_description.lower()
        if "snow" in weather_description or "8" in weather_description or "cold" in weather_description:
            return "Pack: heavy jacket, thermal wear, gloves, boots."
        if "rain" in weather_description or "humid" in weather_description:
            return "Pack: light raincoat, umbrella, breathable clothing."
        return "Pack: light clothing, sunglasses, sunscreen."


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
    kernel.add_plugin(TripPlugin(), plugin_name="Trip")

    history = ChatHistory()
    history.add_user_message(
        "I'm travelling to Manali. Check the weather there and tell me what to pack."
    )

    settings = AzureChatPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    response = await chat_service.get_chat_message_content(
        chat_history=history,
        settings=settings,
        kernel=kernel,
    )

    for msg in history.messages:
        print(f"[{msg.role}]")
        for item in msg.items:
            print(f"   {type(item).__name__}: {item}")

    print("SK -> Azure OpenAI response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())