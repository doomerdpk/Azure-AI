from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-12-01-preview"
)

conversation = [
    {"role": "system", "content": "You are a helpful assistant that answers concisely."}
]

print("Chat started. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=conversation
    )

    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})

    print(f"Assistant: {reply}")
    print(f"(tokens so far: {response.usage.total_tokens})\n")