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


class WeatherPlugin:
    """A trivial native plugin — one function, hardcoded data, no external API call."""

    @kernel_function(
        name="get_weather",
        description="Get the current weather for a given city.",
    )
    def get_weather(self, city: str) -> str:
        fake_data = {
            "mumbai": "32°C, humid, chance of rain",
            "delhi": "38°C, clear skies",
        }
        return fake_data.get(city.lower(), f"No weather data available for {city}.")


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

    # Register the plugin into the kernel so the model can discover and call it
    kernel.add_plugin(WeatherPlugin(), plugin_name="Weather")

    history = ChatHistory()
    history.add_user_message("What's the weather like in Mumbai right now?")

    # Tell SK to let the model auto-decide whether to call a registered function
    settings = AzureChatPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    response = await chat_service.get_chat_message_content(
        chat_history=history,
        settings=settings,
        kernel=kernel,  # kernel must be passed so SK can execute any tool calls the model makes
    )

    print("SK -> Azure OpenAI response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())