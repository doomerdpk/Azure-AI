import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.functions import kernel_function, KernelFunctionFromPrompt
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai import FunctionChoiceBehavior

AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_KEY"]
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


class WeatherPlugin:
    """Native function — deterministic Python code."""

    @kernel_function(
        name="get_weather",
        description="Get the current weather for a given city.",
    )
    def get_weather(self, city: str) -> str:
        fake_data = {
            "mumbai": "32°C, humid, chance of rain",
            "manali": "8°C, snowing",
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

    # Native function plugin
    kernel.add_plugin(WeatherPlugin(), plugin_name="Weather")

    # Prompt function plugin — same kernel, registered as a callable "tool" too
    from semantic_kernel.prompt_template import PromptTemplateConfig, InputVariable

    poetic_fn = KernelFunctionFromPrompt(
        function_name="make_poetic",
        plugin_name="Style",
        description="Rewrite a short piece of text in a poetic, evocative style.",
        prompt_template_config=PromptTemplateConfig(
            name="make_poetic",
            template="Rewrite the following in one poetic, evocative sentence:\n\n{{$input}}",
            input_variables=[
                InputVariable(
                    name="input",
                    description="Text to rewrite poetically",
                    is_required=True,
                    allow_dangerously_set_content=True,  # opt-in: we trust this content (our own tool output)
                )
            ],
            execution_settings={
                "aoai-learning-01": AzureChatPromptExecutionSettings(
                    service_id="aoai-learning-01",
                    max_completion_tokens=600,
                )
            },
        ),
    )
    kernel.add_function(plugin_name="Style", function=poetic_fn)

    history = ChatHistory()
    history.add_user_message(
        "Check the weather in Manali, then rewrite that weather description poetically."
    )

    settings = AzureChatPromptExecutionSettings(
        service_id="aoai-learning-01",
        max_completion_tokens=1500,
    )
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    response = await chat_service.get_chat_message_content(
        chat_history=history,
        settings=settings,
        kernel=kernel,
    )

    print("SK -> Azure OpenAI response:")
    print(response)

    print("--- Trace ---")
    for msg in history.messages:
        print(f"[{msg.role}]")
        for item in msg.items:
            print(f"   {type(item).__name__}: {item}")


if __name__ == "__main__":
    asyncio.run(main())