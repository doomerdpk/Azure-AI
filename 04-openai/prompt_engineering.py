import os, json
from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-12-01-preview"
)

# Prompt Engineering: Response Format
# response = client.chat.completions.create(
#     model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
#     response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant. Always respond with valid JSON."},
#         {"role": "user", "content": "Give me 3 Azure AI Services with a one-line description each. Return as JSON with a 'services' array, each item having 'name' and 'description' fields."}
#     ]
# )

# raw = response.choices[0].message.content
# parsed = json.loads(raw)
# print(json.dumps(parsed, indent=2))



# Prompt Engineering: Few-Shot Prompting
response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "You classify customer support tickets into exactly one category: Billing, Technical, Account, or General."},
        {"role": "user", "content": "I was charged twice this month."},
        {"role": "assistant", "content": "Billing"},
        {"role": "user", "content": "The app crashes when I upload a file."},
        {"role": "assistant", "content": "Technical"},
        {"role": "user", "content": "I can't remember my password and the reset email isn't arriving."},
        {"role": "assistant", "content": "Account"},
        {"role": "user", "content": "My invoice shows a charge for a service I never signed up for."}
    ]
)

print("Classification:", response.choices[0].message.content)