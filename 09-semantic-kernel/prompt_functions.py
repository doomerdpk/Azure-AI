import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.functions import KernelFunctionFromPrompt

AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_KEY"]
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


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

    # A prompt function: a reusable, parameterized prompt template.
    # {{$input}} is SK's templating syntax for a variable slot.
    summarize_fn = KernelFunctionFromPrompt(
        function_name="summarize_in_one_line",
        plugin_name="TextTools",
        prompt="Summarize the following text in exactly one short sentence:\n\n{{$input}}",
        prompt_execution_settings=AzureChatPromptExecutionSettings(
            service_id="aoai-learning-01",
            max_completion_tokens=500,
        ),
    )

    # Register it into the kernel just like a native function
    kernel.add_function(plugin_name="TextTools", function=summarize_fn)

    long_text = (
        "Semantic Kernel is an open-source SDK from Microsoft that lets developers "
        "combine large language models with conventional programming languages. "
        "It provides abstractions for prompts, native code functions, memory, "
        "and orchestration so that both can be composed together into AI-first "
        "applications, agents, and automated workflows."
    )

    # Invoke it directly through the kernel — no chat loop, no tool-calling needed here
    result = await kernel.invoke(summarize_fn, input=long_text)

    print("Prompt function result:")
    print(result)
    print("\n--- Debug: full metadata ---")
    print(result.metadata if hasattr(result, "metadata") else "no metadata attr")


if __name__ == "__main__":
    asyncio.run(main())