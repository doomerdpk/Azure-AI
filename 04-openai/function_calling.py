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
                    "city": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_azure_resource_cost",
            "description": "Get the estimated monthly cost of an Azure resource type",
            "parameters": {
                "type": "object",
                "properties": {
                    "resource_type": {
                        "type": "string",
                        "description": "Azure resource type e.g. Virtual Machine, Storage Account, Azure OpenAI"
                    },
                    "tier": {
                        "type": "string",
                        "description": "Pricing tier e.g. Basic, Standard, Premium"
                    }
                },
                "required": ["resource_type"]
            }
        }
    }
]

# messages = [
#     {"role": "user", "content": "What's the weather like in Mumbai right now?"}
# ]

# response = client.chat.completions.create(
#     model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
#     messages=messages,
#     tools=tools,
#     tool_choice="auto"
# )

# print("Finish reason:", response.choices[0].finish_reason)
# print("Tool calls:", response.choices[0].message.tool_calls)

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

def get_azure_resource_cost(resource_type, tier="Standard"):
    costs = {
        "Virtual Machine": {"Basic": 30, "Standard": 70, "Premium": 150},
        "Storage Account": {"Basic": 5, "Standard": 20, "Premium": 50},
        "Azure OpenAI": {"Basic": 10, "Standard": 50, "Premium": 200},
    }
    cost = costs.get(resource_type, {}).get(tier, 40)
    return {"resource_type": resource_type, "tier": tier, "estimated_monthly_cost_usd": cost}

# tool_call = response.choices[0].message.tool_calls[0]
# args = json.loads(tool_call.function.arguments)
# result = get_weather(**args)
# print("Function result:", result)

# messages.append(response.choices[0].message)
# messages.append({
#     "role": "tool",
#     "tool_call_id": tool_call.id,
#     "content": json.dumps(result)
# })

# final_response = client.chat.completions.create(
#     model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
#     messages=messages,
#     tools=tools
# )

# print("\nFinal reply:", final_response.choices[0].message.content)


for user_message in [
    "What's the weather in Delhi?",
    "How much does a Standard Azure OpenAI deployment cost per month?"
]:
    print(f"\nUser: {user_message}")
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[{"role": "user", "content": user_message}],
        tools=tools,
        tool_choice="auto"
    )
    tool_call = response.choices[0].message.tool_calls[0]
    print(f"Tool selected: {tool_call.function.name}")
    print(f"Arguments: {tool_call.function.arguments}")




