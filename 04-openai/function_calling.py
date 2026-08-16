from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os, json
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-12-01-preview"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name e.g. Mumbai"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

messages = [
    {"role": "user", "content": "What's the weather like in Mumbai right now?"}
]

response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

print("Finish reason:", response.choices[0].finish_reason)
print("Tool calls:", response.choices[0].message.tool_calls)

import random

def get_weather(city, unit="celsius"):
    # Simulated weather data (no real API needed)
    temp = random.randint(28, 35) if unit == "celsius" else random.randint(82, 95)
    return {
        "city": city,
        "temperature": temp,
        "unit": unit,
        "condition": "Humid and partly cloudy",
        "humidity": "78%"
    }

tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
result = get_weather(**args)
print("Function result:", result)

messages.append(response.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": json.dumps(result)
})

final_response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=messages,
    tools=tools
)

print("\nFinal reply:", final_response.choices[0].message.content)