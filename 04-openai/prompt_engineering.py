import os, json
from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-12-01-preview"
)

response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Always respond with valid JSON."},
        {"role": "user", "content": "Give me 3 Azure AI Services with a one-line description each. Return as JSON with a 'services' array, each item having 'name' and 'description' fields."}
    ]
)

raw = response.choices[0].message.content
parsed = json.loads(raw)
print(json.dumps(parsed, indent=2))